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
        res = self.serial.read(9)
        if len(res) == 9:
            checksum = 0xff & (~(res[1] + res[2] + res[3] + res[4] + res[5] + res[6] + res[7]) + 1)
            if res[8] == checksum:
                return (res[2] << 8) | res[3]
        return -1


if __name__ == "__main__":
    sensor = MHZ14A()
    while True:
        print("{}: CO2: {} ppm".format(time.asctime(time.localtime(time.time())), sensor.get_co2level()))
        time.sleep(10)
