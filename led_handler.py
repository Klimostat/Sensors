from machine import Pin

LED_SRV, LED_CO2, LED_RELH = Pin(32, Pin.OUT), Pin(26, Pin.OUT), Pin(27, Pin.OUT)


def init():
    srv_led_off()
    co2_led_off()
    relh_led_off()


# SRV LED
def srv_led_on():
    LED_SRV.value(1)


def srv_led_off():
    LED_SRV.value(0)


def srv_led_get_state():
    return LED_SRV.value()


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


def all_on():
    srv_led_on()
    co2_led_on()
    relh_led_on()


def all_off():
    srv_led_off()
    co2_led_off()
    relh_led_off()
