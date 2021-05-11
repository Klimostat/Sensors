import wifi_connect
import thresholds
import utime
import configurations
import ujson
import urequests
import uerrno
import gc
from machine import Pin, SoftI2C
from scd30 import SCD30


def main():
    wifi_connect.connect()
    thresholds.update_thresholds()

    url = "{}receive.php".format(configurations.API_ENDPOINT)
    headers = {"content-type": "application/x-www-form-urlencoded"}

    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    scd30 = SCD30(i2c, addr=0x61)

    while True:
        last_time = utime.time()

        try:
            while scd30.get_status_ready() != 1:
                utime.sleep_ms(200)
            co2, temp, relh = scd30.read_measurement()

            data = "data=" + ujson.dumps({
                "id": configurations.STATION_ID,
                "token": configurations.TOKEN,
                "co2": co2,
                "temp": temp,
                "relh": relh
            })
            print(data)
            try:
                thresholds_obj = ujson.loads(urequests.post(url, headers=headers, data=data).text)
                thresholds.update_thresholds(thresholds_obj)
            except ValueError:
                # TODO: Serververbindung fehlgeschlagen
                pass

            gc.collect()
            utime.sleep(last_time + configurations.INTERVAL - utime.time())
        except OSError as err:
            print("An error occurred: {}".format(uerrno.errorcode[err.args[0]]))


if __name__ == "__main__":
    main()
