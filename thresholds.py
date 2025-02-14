import urequests
import ujson
import uio
import utime
import configurations
import controller
import led_handler


def update_thresholds(json_data=None):
    print("{}: Updating Thresholds".format(utime.time()))
    if json_data is None:
        if not configurations.WLAN.isconnected():
            print("{}: No wifi connection".format(utime.time()))
            led_handler.srv_led_on()
            return

        url = "{}getThresholds.php".format(configurations.API_ENDPOINT)

        data = "data=" + ujson.dumps({
            "id": configurations.STATION_ID,
            "token": configurations.TOKEN
        })
        print("{}: Downloading threshold data".format(utime.time()))
        try:
            json_data = ujson.loads(urequests.post(url, headers=configurations.HEADERS, data=data).text)
        except Exception as err:
            controller.handle_exception(err)
            led_handler.srv_led_on()
            return

    if not sorted(get_thresholds().items()) == sorted(json_data.items()):
        print("{}: Writing threshold update".format(utime.time()))
        thresholds_obj = uio.open("thresholds.json", "w")
        ujson.dump(json_data, thresholds_obj)
        thresholds_obj.close()
    else:
        print("{}: No threshold update necessary".format(utime.time()))


def get_thresholds():
    thresholds_obj = uio.open("thresholds.json", "r")
    json_data = ujson.load(thresholds_obj)
    thresholds_obj.close()
    return json_data


def check_thresholds(co2, relh):
    thresh = get_thresholds()

    if co2 >= float(thresh["co2"]):
        print("Turned co2 led on")
        led_handler.co2_led_on()
    else:
        print("Turned co2 led off")
        led_handler.co2_led_off()

    if relh <= float(thresh["humidity"]):
        led_handler.relh_led_on()
        print("Turned relh led on")
    else:
        led_handler.relh_led_off()
        print("Turned relh led off")
