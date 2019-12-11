from machine import Pin, I2C
import ssd1306

from utime import sleep, sleep_ms
from display_addons import bigText

# Set the pins on the ESP32
# When a button is pressed, the respective pin is driven low
pinA = Pin(15, Pin.IN)
pinB = Pin(32, Pin.IN)
pinC = Pin(14, Pin.IN)

# Flags --> if 1, button was pressed
flagA = False
flagB = False
flagC = False

alarmDuration = 10 # number of seconds the alarm 'rings'


i2c = I2C(-1, scl=Pin(22), sda=Pin(23))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.poweron()
oled.clearScreen()


# Construct the string to display to the screen
def display(oled, minutes, seconds):

    # clear / reset displayString
    displayString = ""

    if(minutes < 9):
        displayString += "0" + str(minutes)
    else:
        displayString += str(minutes)

    displayString += ":"

    if(seconds < 9):
        displayString += "0" + str(seconds)
    else:
        displayString += str(seconds)

    bigText(oled, displayString, 3, 0, 0, 0)
    oled.show()

def alarm(oled):
    for i in range(alarmDuration):
        oled.clearScreen()
        sleep(1)
        oled.fillWhite()
        sleep(1)

# Input:
# - countdown: # minutes to count down from (max 60)
def countdown(oled, countdown):

    global displayCount, displayMinutes, displaySeconds
    global flagC
    displayCount = countdown * 60 # displayCount is in seconds
    displayMinutes = countdown
    displaySeconds = 0

    #display(oled, displayMinutes, displaySeconds)

    while((displayCount > 0) and (flagC != True)):

        sleep_ms(800) # sleep for roughly 800ms

        oled.clearScreen()
        display(oled, displayMinutes, displaySeconds)

        if((displaySeconds % 60) == 0):
            displayMinutes -= 1 # update minutes

        displayCount -= 1 # decrement the counter every second

        displaySeconds = displayCount % 60 # update seconds

    if(flagC != True):
        alarm(oled)
    else:
        flagC = False # reset the flag
        oled.clearScreen()



def setTimer(oled):
    # A is increment, B is start, C is exit

    global flagA, flagB, flagC

    usercount = 0
    timer = 0
    oled.clearScreen()
    display(oled, timer, 0)

    while((not flagB) and (not flagC)):

        if(flagA == True):
            flagA = False
            usercount += 1
            timer = usercount % 60
            oled.clearScreen()
            display(oled, timer, 0)

    # If B pressed --> start timer
    if(flagB == True):
        flagB = False
        countdown(oled, timer)

    if(flagC == True):
        flagC = False
        oled.clearScreen()


# Define ISRs
# ISR: button A pressed
def APressed(pinA):
    global flagA
    flagA = True

# ISR: button A pressed
def BPressed(pinB):
    global flagB
    flagB = True

# ISR: button C pressed
def CPressed(pinC):
    global flagC
    flagC = True

# Define each pin's interrupt service routine
pinA.irq(trigger=Pin.IRQ_FALLING, handler=APressed)
pinB.irq(trigger=Pin.IRQ_FALLING, handler=BPressed)
pinC.irq(trigger=Pin.IRQ_FALLING, handler=CPressed)

setTimer(oled)
