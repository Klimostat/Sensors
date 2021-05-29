import network
import utime
import configurations
import led_handler


def connect():
    configurations.WLAN = network.WLAN(network.STA_IF)

    if configurations.WLAN.isconnected():
        print("{}: WIFI Already connected".format(utime.time()))
        return True

    configurations.WLAN.active(True)
    configurations.WLAN.connect(configurations.WIFI_SSID, configurations.WIFI_PASSWD)

    for _ in range(10):
        if configurations.WLAN.isconnected():
            break
        utime.sleep_ms(500)

    if configurations.WLAN.isconnected():
        print("{}: WIFI Connection successful".format(utime.time()))
        print(configurations.WLAN.ifconfig())
        return True
    else:
        print("{}: WIFI Connection could not be formed".format(utime.time()))
    return False

