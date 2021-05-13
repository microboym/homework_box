try:

    import RPi.GPIO as GPIO

    INPUT_PIN = 14

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INPUT_PIN, GPIO.IN)


    def book_passed():
        return GPIO.input(INPUT_PIN)

except ImportError:

    def book_passed():
        return True
