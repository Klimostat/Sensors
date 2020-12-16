import time
import board
import adafruit_dht


class DHT11:
    def __init__(self, port=board.D26):
        self.dhtDevice = adafruit_dht.DHT11(port, use_pulseio=False)

    def get_temperature(self):
        t = None
        while t is None:
            try:
                t = self.dhtDevice.temperature
            except:
                continue
        return t

    def get_humidity(self):
        h = None
        while h is None:
            try:
                h = self.dhtDevice.humidity
            except:
                continue
        return h


if __name__ == "__main__":
    dht11 = DHT11()

    while True:
        temperature = dht11.get_temperature()
        humidity = dht11.get_humidity()
        print("{}: Temp: {:.1f} C    Humidity: {}% ".format(time.asctime(time.localtime(time.time())), temperature,
                                                            humidity))
        time.sleep(10)
