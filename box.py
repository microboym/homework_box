import cv2
import requests
import threading
import time
from datetime import datetime

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: Running on local computer.")

# Servo control
ANGLE_OPEN = 70
ANGLE_CLOSE = 130

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

        r = requests.get(self.server_root + "/students")

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
        id = self.recognizer.predict(image, roi=self.roi)
        print("Predicted:", id)

        self.wait_for_book_dropped()

        r = requests.post(self.server_root + "/submit", data = {
            "student_id": id,
            "homework_id": 0, # TODO homework ID
            "submit_time": datetime.now()
        })

        return r.text
    
    def service(self):
        while True:
            # TODO when homework is passed
            time.sleep(0.1)

            result = self.process_passed_book()
            print(result)

    def start_background(self):
        thread = threading.Thread(target=self.service)
        thread.start()
