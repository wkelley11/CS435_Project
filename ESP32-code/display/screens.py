from machine import Pin, I2C
from time import sleep

import ssd1306
from side_bar import draw_side_bar
from size_convert import bigText

# Web scraping scripts
from get_time import getTime
#from get_stocks import getStocks
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
    time = getTime() # uses the network time
    bigText(oled, time, 3, 0, 0, 0)
    oled.show()

def stockScreen():
    oled.text("Stock", 0, 0)
    oled.show()

def weatherScreen():

    # Get hourly forecast
    temptuple = getWeather()
    temperature = temptuple[0] # string
    forecast_msg = temptuple[1] # string

    oled.text(temperature, 0, 0)
    oled.text(forecast_msg, 0, 15)

    #draw_side_bar(oled)
    oled.show()

# Set the pins on the ESP32
# When a button is pressed, the respective pin is driven low
pinA = Pin(15, Pin.IN)
pinB = Pin(32, Pin.IN)
pinC = Pin(14, Pin.IN)

def setScreen(nextScreen):
    oled.clearScreen() # clear before setting to new screen
    nextScreen = nextScreen
    oled.fill(1)
    sleep(5)

# ISR: button A
def APressed():

    nextScreen = (nextScreen - 1) % numberOfScreens
    setScreen(nextScreen)

# ISR: button B pressed
def BPressed():
    setScreen(nextScreen) # B is refresh button: refresh same screen

# ISR: button C pressed
def CPressed():
    nextScreen = (nextScreen + 1) % numberOfScreens
    setScreen(nextScreen)

# Define each function's interrupt service routine
pinA.irq(trigger=Pin.IRQ_FALLING, handler=APressed)
pinA.irq(trigger=Pin.IRQ_FALLING, handler=BPressed)
pinA.irq(trigger=Pin.IRQ_FALLING, handler=CPressed)
