import RPi.GPIO as GPIO
from time import sleep

SERVO_PIN = 2
IR_PIN_1 = 4
IR_PIN_2 = 3

ANGLE_OPEN = 70
ANGLE_CLOSE = 130

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(IR_PIN_1, GPIO.IN)
GPIO.setup(IR_PIN_2, GPIO.IN)
GPIO.setwarnings(False)

def setServoAngle(servo, angle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()

while True:

    if GPIO.input(IR_PIN_1) == 0: # Book passed
        
        setServoAngle(SERVO_PIN, ANGLE_OPEN)
        interval = 0.1
        max_duration = 0.5

        max_times = max_duration / interval
        count = 0
        while True:
            if GPIO.input(IR_PIN_1) == 1: # Book started to drop
                count += 1
                sleep(0.1)

            if GPIO.input(IR_PIN_2) == 0: # Book dropped
                setServoAngle(SERVO_PIN, ANGLE_CLOSE)
                break

            if count >= max_times: # Book lost
                setServoAngle(SERVO_PIN, ANGLE_CLOSE)
                break

GPIO.cleanup()