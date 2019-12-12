from machine import Pin, I2C
from ntptime import settime
from utime import sleep, localtime

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
