import time
import RPi.GPIO as GPIO

class WaterLevelSensor:

    GPIO.setmode(GPIO.BOARD)

    def __init__(self,IOport = 20):
        self.waterSensorIn = GPIO.setup(IOport, GPIO.IN)



    def detect_water_ingress(self):
        while True:
            if GPIO.input(20):
                print("Waterlevel too high!!!")
            time.sleep(30)
