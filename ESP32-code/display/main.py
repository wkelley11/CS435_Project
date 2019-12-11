from machine import Pin, I2C
from time import sleep, sleep_ms

import ssd1306
from side_bar import draw_side_bar
from display_addons import bigText

# Web scraping scripts
from get_time import getTime
from get_stocks import getStocks, getExchange
from get_Weather import getWeather
from io_api import getMQTTMessage

# Global variables to store data
STOCK_DATA = getStocks("AAPL")
CURRENCY_DATA = getExchange("EUR", "USD")
WEATHER_DATA = getWeather() #temp and description stored as tuple
REFRESH_TIMER = utime.ticks_ms()
MACHINE_TIME = utime.ticks_ms()

def refreshTimer(MACHINE_TIME):

    current_time = utime.ticks_ms()

    if ((current_time - MACHINE_TIME) / 1200000) >= 1:
        #refresh the data only if 20 minutes have passed since last refresh
        STOCK_DATA = getStocks("AAPL")
        CURRENCY_DATA = getExchange("EUR", "USD")
        WEATHER_DATA = getWeather()




firstState = 0 # Default screen at initialization is timeScreen
numberOfStates = 5

states = [
    "timeScreen",
    "stockScreen",
    "currencyScreen",
    "weatherScreen",
    "messageScreen"
]

# Set the pins on the ESP32
# When a button is pressed, the respective pin is driven low
pinA = Pin(15, Pin.IN)
pinB = Pin(32, Pin.IN)
pinC = Pin(14, Pin.IN)

# Flags --> if 1, button was pressed
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

def timeRefresh():

    #while(True): # while loop to lt it refresh itself
    current_time = getTime() # uses the network time
    bigText(oled, current_time, 3, 0, 0, 0)
    oled.show()

def stockRefresh():
    while(True):
        # display current value of Apple stock
        #apple_stock = getStocks("AAPL")
        apple_stock = STOCK_DATA
        string = "AAPL: "
        stock = apple_stock + " USD"
        bigText(oled, string, 2, 0, 0, 0)
        oled.text(stock, 0, 20)
        oled.show()

    while(True):
        if(flagA == True):
            break

def currencyRefresh():
    # display Euro to USD exchange rate
    #er = getExchange("EUR", "USD")
    er = CURRENCY_DATA
    bigText(oled, "EUR->USD", 2, 0, 0, 0)
    oled.text(er, 0, 20)
    oled.show()

def weatherRefresh():

    # Get hourly forecast
    #temptuple = getWeather()
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

    global firstState, states # get the global list of states
    nextState = firstState

    refreshTimer(MACHINE_TIME)
    MACHINE_TIME = utime.ticks_ms()

    while(True):

        if(states[nextState] == "timeScreen"): timeRefresh()
        elif(states[nextState] == "stockScreen"): stockRefresh()
        elif(states[nextState] == "currencyScreen"): currencyRefresh()
        elif(states[nextState] == "weatherScreen"): weatherRefresh()
        elif(states[nextState] == "messageScreen"): messageRefresh()

        currentState = nextState
        nextState = getNextState(currentState)
        #checkTimeElapsed()


######################################################


# ISR: button A pressed
def APressed(pinA):
    global flagA
    flagA = True

# ISR: button C pressed
def CPressed(pinC):
    global flagC
    flagC = True

# Define each pin's interrupt service routine
pinA.irq(trigger=Pin.IRQ_FALLING, handler=APressed)
#pinB.irq(trigger=Pin.IRQ_FALLING, handler=BPressed)
pinC.irq(trigger=Pin.IRQ_FALLING, handler=CPressed)
