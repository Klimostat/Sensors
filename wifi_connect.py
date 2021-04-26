def connect():
	import network
	import time
	import configurations

	wlan = network.WLAN(network.STA_IF)

	if wlan.isconnected():
		print("WIFI Already connected")
		return

	wlan.active(True)
	wlan.connect(configurations.WIFI_SSID, configurations.WIFI_PASSWD)

	while not wlan.isconnected():
		time.sleep(0.5)

	print("WIFI Connection successful")
	print(wlan.ifconfig())
