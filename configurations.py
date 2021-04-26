import uio
import ujson

STATION_ID = 1
TOKEN = "asdf"
INTERVAL = 10

WIFI_SSID = ""
WIFI_PASSWD = ""

def get_thresholds():
    thresholds = uio.open("thresholds.json", "w")
    json_data = ujson.load(thresholds)
    thresholds.close()
    return json_data
