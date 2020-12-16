import serial
import time


class MHZ14A:
    request = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]

    def __init__(self, port="/dev/ttyS0"):
        self.serial = serial.Serial(
            port=port,
            timeout=1
        )

    def get_co2level(self):
        self.serial.write(bytearray(self.request))
        response = self.serial.read(9)
        if len(response) == 9:
            return (response[2] << 8) | response[3]
        return -1


if __name__ == "__main__":
    # other Pi versions might need CO2Sensor("/dev/ttyAMA0")
    sensor = MHZ14A()
    while True:
        print("{}: CO2: {} ppa".format(time.asctime(time.localtime(time.time())), sensor.get_co2level()))
        time.sleep(10)
