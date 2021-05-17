import wifi_connect
import thresholds
import utime
import configurations
import ujson
import urequests
import uerrno
import gc
import led_handle
from machine import Pin, SoftI2C
from scd30 import SCD30


def main():
    wifi_connect.connect()
    thresholds.update_thresholds()

    headers = {"content-type": "application/x-www-form-urlencoded"}

    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    scd30 = SCD30(i2c, addr=0x61)

    while True:
        while True:
            try:
                if not scd30.get_status_ready() != 1:
                    break
            except OSError as err:
                print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))

            print("{}: Sensor not ready".format(utime.time()))

            url = "{}ping.php".format(configurations.API_ENDPOINT)
            data = "data=" + ujson.dumps({
                "id": configurations.STATION_ID,
                "token": configurations.TOKEN
            })

            try:
                urequests.post(url, headers=headers, data=data)
            except OSError as err:
                print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
                led_handle.srv_led_on()
            gc.collect()
            utime.sleep(8)

        last_time = utime.time()

        try:
            co2, temp, relh = scd30.read_measurement()
        except OSError as err:
            print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
            continue

        if not configurations.WLAN.isconnected():
            led_handle.srv_led_on()
            continue
        led_handle.srv_led_off()

        url = "{}receive.php".format(configurations.API_ENDPOINT)
        data = "data=" + ujson.dumps({
            "id": configurations.STATION_ID,
            "token": configurations.TOKEN,
            "co2": co2,
            "temp": temp,
            "relh": relh
        })
        print(data)
        try:
            print("{}: Sending data to server".format(utime.time()))
            thresholds_obj = ujson.loads(urequests.post(url, headers=headers, data=data).text)
            thresholds.update_thresholds(thresholds_obj)
        except ValueError as err:
            print("{}: JSON parsen fehlgeschlagen".format(utime.time()))
            led_handle.srv_led_on()
        except OSError as err:
            if err.args[0] == uerrno.ECONNRESET:
                # TODO: Serververbindung fehlgeschlagen
                print("{}: Serververbindung fehlgeschlagen".format(utime.time()))
                led_handle.srv_led_on()
            else:
                print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
                led_handle.srv_led_off()

        gc.collect()
        utime.sleep(last_time + configurations.INTERVAL - utime.time())


if __name__ == "__main__":
    main()
