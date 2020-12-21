import time
import RPi.GPIO as GPIO

class WaterLevelSensor:

    GPIO.setmode(GPIO.BOARD)

    def __init__(self,ioport = 20):
        self.waterSensorIn = GPIO.setup(ioport, GPIO.IN)

    def detect_water_ingress(self):
        while True:
            if self.waterSensorIn.input(20):
                print("Wateringress detected!!!")
            else:
                print("No Wateringress detected.")
            time.sleep(30)

    if __name__ == "__main__":
        while True:
            detect_water_ingress()
