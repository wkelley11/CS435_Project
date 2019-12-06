from machine import Pin, I2C
from time import sleep

import ssd1306
from side_bar import draw_side_bar
from size_convert import bigText

# Web scraping scripts
from get_time import getTime
from get_stocks import getStocks, getExchange
from get_Weather import getWeather

nextScreen = 0 # Default screen at initialization is timeScreen
numberOfScreens = 3

# Initialize the OLED
# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(23))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.poweron()
oled.clearScreen()
oled.stopScroll()


def timeScreen():

    #while(True): # while loop to lt it refresh itself
    time = getTime() # uses the network time
    bigText(oled, time, 3, 0, 0, 0)
    oled.show()

    sleep(15) # refresh every fifteen seconds
    timeScreen()

    #if(getTime()[4] != time[4]):
    #     timeScreen() # refresh every thirty seconds

def stockScreen():
    # apple_stock = getStocks("AAPL")
    # string = "AAPL: "
    # stock = apple_stock + " USD"
    # bigText(oled, string, 2, 0, 0, 0)
    # oled.text(stock, 0, 20)
    # oled.show()

    # display Euro to USD exchange rate
    er = getExchange("EUR", "USD")
    bigText(oled, "EUR->USD", 2, 0, 0, 0)
    oled.text(er, 0, 20)
    oled.show()

def weatherScreen():

    # Get hourly forecast
    temptuple = getWeather()
    temperature = temptuple[0] # string
    forecast_msg = temptuple[1] # string

    oled.text(temperature + " F", 0, 0)
    oled.text(forecast_msg, 0, 15)

    #draw_side_bar(oled)
    oled.show()

# Set the pins on the ESP32
# When a button is pressed, the respective pin is driven low
pinA = Pin(15, Pin.IN)
pinB = Pin(32, Pin.IN)
pinC = Pin(14, Pin.IN)

# Initialize default screen to time
timeScreen()

def setScreen(nextScreen):

    oled.clearScreen()

    screens = [
        timeScreen,
        stockScreen,
        weatherScreen
    ]

    fct = screens[nextScreen]
    fct()


# ISR: button A pressed
def APressed(pinA):

    global nextScreen
    global numberOfScreens

    nextScreen = (nextScreen - 1) % numberOfScreens
    setScreen(nextScreen)


# ISR: button B pressed
def BPressed(pinB):

    global nextScreen

    setScreen(nextScreen) # B is refresh button: refresh same screen

# ISR: button C pressed
def CPressed(pinC):

    global nextScreen

    nextScreen = (nextScreen + 1) % numberOfScreens
    setScreen(nextScreen)

# Define each pin's interrupt service routine
pinA.irq(trigger=Pin.IRQ_FALLING, handler=APressed)
pinB.irq(trigger=Pin.IRQ_FALLING, handler=BPressed)
pinC.irq(trigger=Pin.IRQ_FALLING, handler=CPressed)
