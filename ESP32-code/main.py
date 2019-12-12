from machine import Pin, I2C
from utime import sleep, sleep_ms, ticks_ms()

# Display scrips
import display.ssd1306
from display.side_bar import draw_side_bar
from display.add_ons import bigText, displayTimeFormat, scrollLeft

# API / Web collection scripts
from data.get_time import getTime
from data.get_stocks import getStocks, getExchange
from data.get_Weather import getWeather
from data.get_iomessage import getMQTTMessage

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
MACHINE_TIME = ticks_ms()

# Gathers new data from APIs to update global data variables
def refreshData(time):

    current_time = ticks_ms()

    # Refresh the data only if 20 minutes have passed since the last refresh
    #if(((current_time - time) / 1200000) >= 1):
    if(((current_time - time) / 10000) >= 1):
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

# Number of times the alarm 'rings'
alarmDuration = 10

# 'Alarm' for the timer: intermittently goes all blank and all black
# for alarmDuration number of times
def alarm(oled):
    global flagC, flagA, flagB

    for i in range(alarmDuration):

        oled.clearScreen()

        if((flagA == True) or (flagC == True) or (flagB == True)): # stop alarm
            # lower the flags
            flagA = False
            flagB = False
            flagC = False
            break

        sleep(1)
        oled.fillWhite()
        sleep(1)

# Input: oled, countdown: # minutes to count down from (max 60)
def countdown(oled, countdown):

    global displayCount, displayMinutes, displaySeconds
    global flagA, flagB, flagC

    displayCount = countdown * 60 # displayCount is in seconds
    displayMinutes = countdown
    displaySeconds = 0

    while(flagC != True): # Pause loop

        while((displayCount >= 0) and (flagC != True) and (flagB != True)):

            sleep_ms(850)

            oled.clearScreen()
            displayTimeFormat(oled, displayMinutes, displaySeconds)

            if((displaySeconds % 60) == 0): # if it's been a minute
                displayMinutes -= 1 # update minutes

            displayCount -= 1 # decrement the counter every second
            displaySeconds = displayCount % 60 # update seconds

        if(displayCount <= 0): # if time is up
            alarm(oled)
            break
        elif(flagC == True): # don't reset the flag yet, so we fully exit from timer
            oled.clearScreen()
            break
        elif(flagB == True): # flag B raised – Pause timer
            flagB = False # reset the Flag
            while((flagB != True) and (flagC != True)): continue # get stuck in a while loop
        else: # error handling (just in case)
            oled.clearScreen()
            flagC = True # so that we fully exit from timer afterwards
            break

        if(flagB == True):
            flagB = False # lower the flag to resume countdown

    # Lower any flags
    if(flagA == True):
        flagA = False
    if(flagC == True):
        flagC = False


def setTimer(oled):
    # A is increment, B is start, C is exit

    global flagA, flagB, flagC

    usercount = 0
    timer = 0
    oled.clearScreen()
    displayTimeFormat(oled, timer, 0)

    while((not flagB) and (not flagC)):

        # If A pressed: increment the timer set by 1
        if(flagA == True):
            flagA = False
            usercount += 1
            timer = usercount % 60
            oled.clearScreen()
            displayTimeFormat(oled, timer, 0)

    # If B pressed: start timer
    if(flagB == True):
        flagB = False
        countdown(oled, timer)

    # If C pressed --> exit the timer, break from loop
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

    oled.show()

def messageRefresh():
    # Display latest message from Adafruit IO broker
    message = getMQTTMessage()

    if(len(message) > 15): # too long for screen!
        while((not flagA) and (not flagC)):
            formatted_msg = "Last MQTT msg:" + message
            scrollLeft(oled, formatted_msg, 0, 15)

    else:
        oled.text("Last MQTT msg:", 0, 0)
        oled.text(message, 0, 15)
        oled.show()

def countdownTimer():

    global flagB

    draw_side_bar(oled)
    options = "B: Set timer."
    oled.text(options, 0, 12)
    oled.show()

    # B pressed: user wishes to access the timer
    if(flagB == True):
        flagB = False # lower flag

        oled.clearScreen()
        oled.text("A: timer set +1", 0, 0)
        oled.text("B: start/pause", 0, 10)
        oled.text("C: exit", 0, 20)
        oled.show()

        sleep(3)

        # In case user pressed buttons: lower the flags
        flagA = False
        flagB = False
        flagC = False

        setTimer(oled)


#######################################################


# Initialize the OLED
# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(23))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.poweron()
oled.clearScreen()


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

    if(flagB == True):
        flagB = False # default reset the flag

    # C was pressed
    if(flagC == True):
        nextState = (currentState + 1) % numberOfStates
        flagC = False # reset the flag until button C is pressed again


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
        MACHINE_TIME = ticks_ms()

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
