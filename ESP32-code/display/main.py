# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, I2C
import ssd1306
from time import sleep

# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(23))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.poweron()

oled.stopScroll() # Scroll must be stopped before initiating a scroll command!

# 2nd param: x-coord from left edge
# 3rd param: y-coord from top edge
oled.text('Hello world 1!', 0, 10)
oled.show()

sleep(2)

oled.scrollHorizontal()

sleep(5)

oled.stopScroll() # Scroll must be stopped before initiating a scroll command!

# sleep(2)
#
# oled.scrollHorizontal() # scroll the screen
# sleep(5)
# oled.stopScroll() # Scroll must be stopped before initiating a scroll command!
#
# sleep(5)


# oled.clearScreen()
#
# oled.text('Hey hey trying', 0, 0)
# oled.text('trying again!', 0, 10)
# oled.show()
#
# sleep(5)

oled.poweroff()
