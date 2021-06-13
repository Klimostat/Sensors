set -x

mpy-cross -march=xtensawin controller.py
mpy-cross -march=xtensawin led_handler.py
mpy-cross -march=xtensawin thresholds.py
mpy-cross -march=xtensawin wifi_connect.py
mpy-cross -march=xtensawin urequests.py
mpy-cross -march=xtensawin scd30.py

ampy -p /dev/ttyUSB0 put controller.mpy
ampy -p /dev/ttyUSB0 put led_handler.mpy
ampy -p /dev/ttyUSB0 put thresholds.mpy
ampy -p /dev/ttyUSB0 put wifi_connect.mpy
ampy -p /dev/ttyUSB0 put scd30.py

rm *.mpy
