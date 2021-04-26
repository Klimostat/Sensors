import wifi_connect
wifi_connect.connect()

import time
import configurations
import ujson
import urequests
from sdc30 import SDC30


url = "https://home.letusflow.at/api/receive.php"
headers = {"content-type": "application/x-www-form-urlencoded"}

sdc = SDC30()

while True:
    last_time = time.time()

    data = sdc.read_measurement()

    data = "data=" + ujson.dumps({
        "id": configurations.STATION_ID,
        "token": configurations.TOKEN,
        "measurements": {
            "co2": data[0],
            "temp": data[1],
            "rh": data[2]
        }
    })
    print(urequests.post(url, headers=headers, data=data).text)

    time.sleep(last_time + configurations.INTERVAL - time.time())
