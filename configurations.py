import uio
import ujson

STATION_ID = 1
TOKEN = "asdf"
INTERVAL = 10

WIFI_SSID = "HTLW3R_WLAN"
WIFI_PASSWD = "HTLW3R_WLAN"

def get_thresholds():
    thresholds = uio.open("thresholds.json", "w")
    json_data = ujson.load(thresholds)
    thresholds.close()
    return json_data
