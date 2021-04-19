import wifi_connect
wifi_connect.connect()

import time
import constants
import ujson
import urequests


url = "https://home.letusflow.at/post.php"
headers = {"content-type": "application/x-www-form-urlencoded"}

while True:
    last_time = time.time()

    data = "data=" + ujson.dumps({
        "device": constants.STATION_ID,
        "token": constants.TOKEN,
        "measurements": {
            "sensor1": "value1",
            "sensor2": "value1"
        }
    })
    print(urequests.post(url, headers=headers, data=data).text)

    time.sleep(last_time + constants.INTERVAL - time.time())
