import network
import time
import configurations


def connect():
    configurations.WLAN = network.WLAN(network.STA_IF)

    if configurations.WLAN.isconnected():
        print("WIFI Already connected")
        return

    configurations.WLAN.active(True)
    configurations.WLAN.connect(configurations.WIFI_SSID, configurations.WIFI_PASSWD)

    for _ in range(10):
        if configurations.WLAN.isconnected():
            break
        time.sleep(0.5)

    print("WIFI Connection successful")
    print(configurations.WLAN.ifconfig())
