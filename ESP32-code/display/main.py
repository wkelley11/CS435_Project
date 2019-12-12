from machine import Pin, I2C
from time import sleep, sleep_ms
import utime

import ssd1306
from side_bar import draw_side_bar
from display_addons import bigText, displayTimeFormat

# API / Web collection scripts
from get_time import getTime
from get_stocks import getStocks, getExchange
from get_Weather import getWeather
from get_iomessage import getMQTTMessage

firstState = 0 # Default screen at initialization is timeScreen
numberOfStates = 6

states = [
    "timeScreen",
    "stockScreen",
    "currencyScreen",
    "weatherScreen",
    "messageScreen",
    "countdownScreen"
]

# Global variables to store data
STOCK_DATA = getStocks("AAPL") # returns a string
CURRENCY_DATA = getExchange("EUR", "USD") # returns a string
WEATHER_DATA = getWeather() # Temperature & weather description (e.g. "sunny") returned as tuple

# Global variable which stores a timestamp
MACHINE_TIME = utime.ticks_ms()

# Gathers new data from APIs to update global data variables
def refreshData(time):

    current_time = utime.ticks_ms()

    # Refresh the data only if 20 minutes have passed since the last refresh
    if(((current_time - time) / 1200000) >= 1):
        STOCK_DATA = getStocks("AAPL")
        CURRENCY_DATA = getExchange("EUR", "USD")
        WEATHER_DATA = getWeather()
        return True
    else:
        return False

# Set the ESP32 pins for the buttons / ISRs
# When a button is pressed, the respective pin is driven low
pinA = Pin(15, Pin.IN)
pinB = Pin(32, Pin.IN)
pinC = Pin(14, Pin.IN)

# Flags --> if True, the button was pressed
flagA = False
flagB = False
flagC = False

# Initialize the OLED
# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(23))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.poweron()
oled.clearScreen()
oled.stopScroll()


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

        sleep_ms(850)

        oled.clearScreen()
        displayTimeFormat(oled, displayMinutes, displaySeconds)

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
    displayTimeFormat(oled, timer, 0)

    while((not flagB) and (not flagC)):

        if(flagA == True):
            flagA = False
            usercount += 1
            timer = usercount % 60
            oled.clearScreen()
            displayTimeFormat(oled, timer, 0)

    # If B pressed --> start timer
    if(flagB == True):
        flagB = False
        countdown(oled, timer)

    if(flagC == True):
        flagC = False
        oled.clearScreen()



def timeRefresh():
    #display the current time

    #while(True): # while loop to lt it refresh itself
    current_time = getTime() # uses the network time
    bigText(oled, current_time, 3, 0, 0, 0)
    oled.show()

def stockRefresh():
    #display value of Apple stock
    # display current value of Apple stock
    #apple_stock = getStocks("AAPL")
    apple_stock = STOCK_DATA
    string = "AAPL: "
    stock = apple_stock + " USD"
    bigText(oled, string, 2, 0, 0, 0)
    oled.text(stock, 0, 20)
    oled.show()

def currencyRefresh():
    # display Euro to USD exchange rate

    er = CURRENCY_DATA
    bigText(oled, "EUR->USD", 2, 0, 0, 0)
    oled.text(er, 0, 20)
    oled.show()

def weatherRefresh():
    # Get hourly forecast

    temptuple = WEATHER_DATA
    temperature = temptuple[0] # string
    forecast_msg = temptuple[1] # string

    oled.text(temperature + " F", 0, 0)
    oled.text(forecast_msg, 0, 15)

    #draw_side_bar(oled)
    oled.show()


def messageRefresh():
    # Display latest message from Adafruit IO broker
    message = getMQTTMessage()

    oled.text(message, 0, 0)
    oled.show()

def countdownTimer():

    global flagB

    draw_side_bar(oled)
    options = "B: Set timer."
    oled.text(options, 0, 12)
    oled.show()

    if(flagB == True):
        flagB = False # lower flag
        setTimer(oled)



#######################################################

# Figure out what the next logical state to visit is
def getNextState(currentState):

    global numberOfStates
    global flagA, flagB, flagC

    temp = currentState
    nextState = currentState

    # A was pressed
    if(flagA == True):
        nextState = (currentState - 1) % numberOfStates
        flagA = False # reset the flag until button A is pressed again

    # C was pressed
    elif(flagC == True):
        nextState = (currentState + 1) % numberOfStates
        flagC = False


    if(currentState != nextState):
        oled.clearScreen()

    return nextState


# def updateMQTTMessage():
#     c.check_msg() # Check if an MQTT message was uploaded
#     if (new_msg == True):
#         new_msg = False # reset to false as message is now read
#
# def checkTimeElapsed(currentState):


######################################################

# Setting up main as a state machine
def run():

    global firstState, states  # get the global list of states
    global MACHINE_TIME

    nextState = firstState # set to 0

    # Check if 20 minutes have passed since the last data update
    reset = refreshData(MACHINE_TIME)
    if reset:
        MACHINE_TIME = utime.ticks_ms()

    while(True):

        if(states[nextState] == "timeScreen"): timeRefresh()
        elif(states[nextState] == "stockScreen"): stockRefresh()
        elif(states[nextState] == "currencyScreen"): currencyRefresh()
        elif(states[nextState] == "weatherScreen"): weatherRefresh()
        elif(states[nextState] == "messageScreen"): messageRefresh()
        elif(states[nextState]== "countdownScreen"): countdownTimer()

        currentState = nextState
        nextState = getNextState(currentState)

        sleep_ms(200) # Short delay to prevent button debouncing


######################################################

# ISR functions: raise a flag (True) if button pressed.
# Lower the flag (set to False) elsewhere, once we've processed the flag.

# ISR: button A pressed
def APressed(pinA):
    global flagA
    flagA = True

# ISR: button C pressed
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
