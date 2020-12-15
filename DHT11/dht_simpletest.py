import time
import board
import adafruit_dht

if __name__ == "__main__":
    dhtDevice = adafruit_dht.DHT11(board.D26, use_pulseio=False)

    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print("{}: Temp: {:.1f} C    Humidity: {}% ".format(time.asctime(time.localtime(time.time())), temperature,
                                                                humidity))

        except Exception as error:
            continue

        time.sleep(10)
