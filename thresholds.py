import urequests
import ujson
import uio
import configurations


def update_thresholds(json_data=None):
    if json_data is None:
        if not configurations.WLAN.isconnected():
            return

        url = "{}getThresholds.php".format(configurations.API_ENDPOINT)
        headers = {"content-type": "application/x-www-form-urlencoded"}

        data = "data=" + ujson.dumps({
            "id": configurations.STATION_ID,
            "token": configurations.TOKEN
        })
        json_data = ujson.loads(urequests.post(url, headers=headers, data=data).text)

    thresholds = uio.open("thresholds.json", "w")
    ujson.dump(json_data, thresholds)
    thresholds.close()
