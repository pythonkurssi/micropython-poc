from machine import Pin
from secrets import SSID, WIFI_PASSWORD
import network
import time

red_light = Pin(32, Pin.OUT)
flashlight = Pin(4, Pin.OUT)


def do_connect():
    red_light.value(0)  # on

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, WIFI_PASSWORD)

    while not wlan.isconnected():
        pass

    red_light.value(1)  # off

    print('network config:', wlan.ifconfig())

    return wlan


wlan = do_connect()
