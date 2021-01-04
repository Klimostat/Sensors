import time
import RPi.GPIO as GPIO


class WaterLevelSensor:
    def __init__(self, port=20):
        self.ioport = port
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def detect_water_ingress(self):
        return GPIO.input(self.ioport) == GPIO.HIGH


if __name__ == "__main__":
    water = WaterLevelSensor()
    while True:
        print(water.detect_water_ingress())
        time.sleep(1)
