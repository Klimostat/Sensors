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
    # led blink
    led_handler.all_on()
    utime.sleep_ms(500)
    led_handler.all_off()
    utime.sleep_ms(500)
    led_handler.all_on()
    utime.sleep_ms(500)
    led_handler.all_off()

    led_handler.srv_led_on()
    wifi_connect.connect()
    thresholds.update_thresholds()

    headers = {"content-type": "application/x-www-form-urlencoded"}

    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    scd30 = SCD30(i2c, addr=0x61)

    while True:
        while True:
            last_time = utime.time()
            try:
                sensor_status = scd30.get_status_ready()
                wifi_status = configurations.WLAN.isconnected()
                if sensor_status == 1 and wifi_status:
                    break
                if sensor_status != 1:
                    print("{}: Sensor not ready".format(utime.time()))
                if wifi_status != 1:
                    print("{}: WIFI not ready".format(utime.time()))
            except OSError as err:
                print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
                print("{}: Sensor or WIFI not ready".format(utime.time()))

            url = "{}ping.php".format(configurations.API_ENDPOINT)
            data = "data=" + ujson.dumps({
                "id": configurations.STATION_ID,
                "token": configurations.TOKEN
            })

            try:
                urequests.post(url, headers=headers, data=data)
            except OSError as err:
                if err.args[0] in uerrno.errorcode.keys():
                    print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
                else:
                    print("{}: An error occurred: {}".format(utime.time(), err.args[0]))

            led_handler.srv_led_on()
            gc.collect()
        time_diff = last_time + configurations.INTERVAL - utime.time()
        if time_diff > 1:
            utime.sleep(time_diff)

        last_time = utime.time()

        try:
            co2, temp, relh = scd30.read_measurement()
        except OSError as err:
            print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
            continue

        url = "{}receive.php".format(configurations.API_ENDPOINT)
        data = "data=" + ujson.dumps({
            "id": configurations.STATION_ID,
            "token": configurations.TOKEN,
            "co2": co2,
            "temp": temp,
            "relh": relh
        })
        print("Sensor reading: {}".format(data))
        try:
            print("{}: Sending data to server".format(utime.time()))
            thresholds_obj = ujson.loads(urequests.post(url, headers=headers, data=data).text)
            thresholds.update_thresholds(thresholds_obj)

            led_handler.srv_led_off()

        except ValueError:
            print("{}: failed parsing JSON".format(utime.time()))
            led_handler.srv_led_on()
        except OSError as err:
            print("{}: An error occurred: {}".format(utime.time(), uerrno.errorcode[err.args[0]]))
            led_handler.srv_led_on()

        thresholds.check_thresholds(co2, temp, relh)
        gc.collect()
        time_diff = last_time + configurations.INTERVAL - utime.time()
        if time_diff > 1:
            utime.sleep(time_diff)
