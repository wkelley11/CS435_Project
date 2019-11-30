# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, I2C
import ssd1306
from side_bar import draw_side_bar
from time import sleep

# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(23))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.poweron()
oled.clearScreen()

# Draw up and down side bar arrows
draw_side_bar(oled)
oled.show()

sleep(3)

oled.text('world yo!', 50, 10)
oled.show()

sleep(3)

#oled.stopScroll() # Scroll must be stopped before initiating a scroll command!

#oled.poweroff()


# def text_cut(str):
#
#     if(len(str) < )
