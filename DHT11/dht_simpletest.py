import time
import board
import adafruit_dht


class DHT11:
    def __init__(self, port=board.D26):
        self.dhtDevice = adafruit_dht.DHT11(port, use_pulseio=False)

    def get_temperature(self):
        while True:
            try:
                temperature = self.dhtDevice.temperature
                return temperature
            except Exception:
                continue

    def get_humidity(self):
        while True:
            try:
                humidity = self.dhtDevice.humidity
                return humidity
            except Exception:
                continue


if __name__ == "__main__":
    dht11 = DHT11()

    while True:
        temperature = dht11.get_temperature()
        humidity = dht11.get_humidity()
        print("{}: Temp: {:.1f} C    Humidity: {}% ".format(time.asctime(time.localtime(time.time())), temperature,
                                                            humidity))
        time.sleep(10)
