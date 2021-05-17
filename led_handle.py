from machine import Pin

LED_SRV, LED_TEMP, LED_CO2, LED_RELH = Pin(32, Pin.OUT), \
                                       Pin(33, Pin.OUT),\
                                       Pin(34, Pin.OUT),\
                                       Pin(35, Pin.OUT)


# SRV LED
def srv_led_on():
    LED_SRV.value(1)


def srv_led_off():
    LED_SRV.value(0)


def srv_led_get_state():
    return LED_SRV.value()


# TEMP LED
def temp_led_on():
    LED_TEMP.value(1)


def temp_led_off():
    LED_TEMP.value(0)


def temp_led_get_state():
    return LED_TEMP.value()


# CO2 LED
def co2_led_on():
    LED_CO2.value(1)


def co2_led_off():
    LED_CO2.value(0)


def co2_led_get_state():
    LED_CO2.value()


# SRV LED
def relh_led_on():
    LED_RELH.value(1)


def relh_led_off():
    LED_RELH.value(0)


def relh_led_get_state():
    LED_RELH.value()
