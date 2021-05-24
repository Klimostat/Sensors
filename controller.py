import wifi_connect
import thresholds
import utime
import configurations
import ujson
import urequests
import uerrno
import gc
import led_handler
from machine import Pin, SoftI2C
from scd30 import SCD30


def main():
    led_handler.srv_led_on()
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
                led_handler.srv_led_on()
            gc.collect()
            utime.sleep(8)

        last_time = utime.time()

        try:
            co2, temp, relh = scd30.read_measurement()
        except OSError as err:
            print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
            continue

        if not configurations.WLAN.isconnected():
            led_handler.srv_led_on()
            continue
        led_handler.srv_led_off()

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
            led_handler.srv_led_on()
        except OSError as err:
            if err.args[0] == uerrno.ECONNRESET:
                print("{}: Serververbindung fehlgeschlagen".format(utime.time()))
                led_handler.srv_led_on()
            else:
                print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
                led_handler.srv_led_off()

        check_thresholds(co2, temp, relh)
        gc.collect()
        utime.sleep(last_time + configurations.INTERVAL - utime.time())


def check_thresholds(co2, temp, relh):
    thresh = thresholds.get_thresholds()

    if co2 >= thresh["co2"]:
        led_handler.co2_led_on()
    else:
        led_handler.co2_led_off()

    if temp >= thresh["temp"]:
        led_handler.temp_led_on()
    else:
        led_handler.temp_led_off()

    if temp >= thresh["relh"]:
        led_handler.relh_led_on()
    else:
        led_handler.relh_led_off()
