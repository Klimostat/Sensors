def connect():
	import network
	import time
	import constants

	wlan = network.WLAN(network.STA_IF)

	if wlan.isconnected():
		print("Already connected")
		return

	wlan.active(True)
	wlan.connect(constants.WIFI_SSID, constants.WIFI_PASSWD)

	while not wlan.isconnected():
		time.sleep(0.5)

	print("Connection successful")
	print(wlan.ifconfig())
