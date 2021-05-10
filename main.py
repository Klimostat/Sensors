import wifi_connect

wifi_connect.connect()

import utime
import configurations
import ujson
import urequests
from machine import Pin, SoftI2C
from scd30 import SCD30

url = "{}receive.php".format(configurations.API_ENDPOINT)
headers = {"content-type": "application/x-www-form-urlencoded"}

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
scd30 = SCD30(i2c, addr=0x61)

while True:
    last_time = utime.time()

    while scd30.get_status_ready() != 1:
        utime.sleep_ms(200)
    co2, temp, relh = scd30.read_measurement()

    data = "data=" + ujson.dumps({
        "id": configurations.STATION_ID,
        "token": configurations.TOKEN,
        "measurements": {
            "co2": co2,
            "temp": temp,
            "relh": relh
        }
    })
    print(data)
    print(urequests.post(url, headers=headers, data=data).text)

    utime.sleep(last_time + configurations.INTERVAL - utime.time())
