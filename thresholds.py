import urequests
import ujson
import uio
import utime
import configurations
import led_handler


def update_thresholds(json_data=None):
    print("{}: Updating Thresholds".format(utime.time()))
    if json_data is None:
        if not configurations.WLAN.isconnected():
            print("{}: No wifi connection".format(utime.time()))
            led_handler.srv_led_on()
            return

        url = "{}getThresholds.php".format(configurations.API_ENDPOINT)
        headers = {"content-type": "application/x-www-form-urlencoded"}

        data = "data=" + ujson.dumps({
            "id": configurations.STATION_ID,
            "token": configurations.TOKEN
        })
        print("{}: Downloading threshold data".format(utime.time()))
        try:
            json_data = ujson.loads(urequests.post(url, headers=headers, data=data).text)
        except OSError as err:
            print("{}: An error occurred".format(utime.time()))
            led_handler.srv_led_on()
    if not sorted(get_thresholds().items()) == sorted(json_data.items()):
        print("{}: Writing threshold update".format(utime.time()))
        thresholds_obj = uio.open("thresholds.json", "w")
        ujson.dump(json_data, thresholds_obj)
        thresholds_obj.close()
        led_handler.srv_led_off()
    else:
        print("{}: No threshold update necessary".format(utime.time()))
        led_handler.srv_led_off()


def get_thresholds():
    thresholds_obj = uio.open("thresholds.json", "r")
    json_data = ujson.load(thresholds_obj)
    thresholds_obj.close()
    return json_data
