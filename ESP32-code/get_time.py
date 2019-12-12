from machine import Pin, I2C
from time import sleep

import ssd1306
from side_bar import draw_side_bar
from display_addons import bigText

# Web scraping scripts
#from get_time import getTime
#from get_stocks import getStocks
#from get_Weather import getWeather

# Initialize the OLED
# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(23))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

from ntptime import settime
from utime import localtime

# set the device time using the network, on script import
settime()

# Returns the current time as a string, in hour-hour:minute-minute format.
# This uses the time as defined on the network, so if the network time is off,
# so will this value.
def getTime():

    # convert RTC time to more readable time and date
    (year, month, day, hour, minute, second, weekday, yearday) = localtime()
    #t = localtime()

    hour = (hour % 12) + 7
    hour = str(hour)
    minute = str(minute)

    if(len(hour) == 1):
        hour = "0" + hour
    if(len(minute) == 1):
        minute = "0" + minute

    hhmm = hour + ":" + minute
    return hhmm


def timeScreen():

    oled.clearScreen()
    time = getTime() # uses the network time
    bigText(oled, time, 3, 0, 0, 0)

    oled.show()
