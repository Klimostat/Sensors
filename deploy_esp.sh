set -x

# esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
# esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20210418-v1.15.bin

./compile_and_upload.sh

ampy -p /dev/ttyUSB0 put main.py
ampy -p /dev/ttyUSB0 put thresholds.json
ampy -p /dev/ttyUSB0 put configurations.py

# picocom /dev/ttyUSB0 -b115200
: <<'END'
import wifi_connect
wifi_connect.connect()
import upip
upip.install("micropython-scd30")
upip.install("micropython-urequests")
Ctrl+D
END
