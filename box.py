import cv2
import requests
import threading
import time
import json
from datetime import datetime

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: Running on local computer.")

# Servo control
ANGLE_OPEN = 80
ANGLE_CLOSE = 380

def setServoAngle(servo, angle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    time.sleep(0.3)
    pwm.stop()

class Box:
    
    def __init__(self, recognizer, cam_index, servo_pin, ir_1_pin, ir_2_pin, server_root):
        self.recognizer = recognizer
        self.camera = cv2.VideoCapture(cam_index)
        self.server_root = server_root

        self.set_up_pins(servo_pin, ir_1_pin, ir_2_pin)

        # TODO Request for student list
        # r = requests.get(self.server_root + "/students")
        # self.students = json.loads(r.text)
        test_students = [
            {"id": 70101, "name":"李宇航"},
            {"id": 70102, "name":"温子航"},
            {"id": 70103, "name":"王思悦"},
            {"id": 70104, "name":"任执行"},
            {"id": 70105, "name":"王大友"},
        ]
        self.students = test_students

    def set_up_pins(self, servo_pin, ir_1_pin, ir_2_pin):
        self.servo_pin = servo_pin
        self.ir_1_pin = ir_1_pin
        self.ir_2_pin = ir_2_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        GPIO.setup(self.ir_1_pin, GPIO.IN)
        GPIO.setup(self.ir_2_pin, GPIO.IN)
        GPIO.setwarnings(False)

    def wait_for_book_dropped(self, max_duration=0.5, interval=0.1):
        max_times = max_duration / interval
        count = 0
        while True:
            if GPIO.input(self.ir_1_pin) == 1: # Book started to drop
                count += 1
                time.sleep(interval)

            if GPIO.input(self.ir_2_pin) == 0: # Book dropped
                setServoAngle(self.servo_pin, ANGLE_CLOSE)
                break

            if count >= max_times: # Book lost
                setServoAngle(self.servo_pin, ANGLE_CLOSE)
                break
    
    def process_passed_book(self):
        _, image = self.camera.read()
        cv2.imwrite("temp.jpg", image)
        id = self.recognizer.predict(image)
        print("Predicted:", id)

        self.wait_for_book_dropped()

        # r = requests.post(self.server_root + "/submit", data = {
        #     "student_id": id,
        #     "homework_id": 0, # TODO homework ID
        #     "submit_time": datetime.now()
        # })

        if self.listener is not None:
            for student in self.students:
                if student["id"] == id:
                    self.listener(student["name"])

        # return r.text
    
    def service(self):
        print("Starting service")
        while True:
            # print(GPIO.input(self.ir_1_pin))
            if GPIO.input(self.ir_1_pin) == 0:
                print("Book passed.")
                time.sleep(0.1)

                result = self.process_passed_book()
                print(result)

    def start_background(self):
        thread = threading.Thread(target=self.service)
        thread.start()

    def set_listener(self, listener):
        self.listener = listener
