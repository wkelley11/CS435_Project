import network
from utime import sleep

WIFI_SSID = 'MiddleburyGuest'

def connect():
    """ Setup a connection """
    sta_if = network.WLAN(network.STA_IF)  # Configure as station

    if not sta_if.isconnected():  # If it is not connected
        print('Connecting to ' + WIFI_SSID)
        sta_if.active(True)
        sta_if.connect(WIFI_SSID)
        while not sta_if.isconnected():
            print('.', end='');
    else:  # If we are already connected
        print('Already connected to ' + sta_if.config('essid'))

    # Show the network configuration
    print('network config:', sta_if.ifconfig())

connect()

sleep(2)

from main import *
run()
