# This script provides functions to modify text or character size,
# scroll a string (of standard size) horizontally to the left,
# and display a string in time format ("mm:ss").

from display.font_petme128_8x8 import alphabet
from utime import sleep, sleep_ms

# Function to expand text size by a factor. See fct input:
# - oled object
# - message to display
# - factor (int) by which to expand the string (recommended: 2 or 3)
# - x and y top-left start coordinates of 1st character
# - spacing to put between each character
def bigText(oled, message, factor, x_start, y_start, spacing):

    x = x_start
    y = y_start
    for char in message:
        asc = ord(char)
        byte = alphabet[asc - 32]
        bigChar(oled, byte, factor, x, y)
        x += (factor * 8)

# Expands the size of a single character by a given factor.
# Function called in bigText(...).
def bigChar(oled, bits, factor, x, y):

    for i in range(len(bits)): # For every row (i.e. byte) in matrix 'bits'
        for b in range(8): # for every bit in a byte
            for row in range(factor):
                for col in range(factor):
                    oled.pixel((factor * i) + row + x, (factor * b) + col + y, bits[i]&(0x01<<b))


# Scrolls the text off to the left of the screen
def scrollLeft(oled, str, x, y):
    for i in range(len(str)): # for every character

        oled.text(str[i:], x, y) # display from character i to the end
        oled.show()

        for j in range(8): # for every pixel in the character

            oled.scroll(-1,0) # x_step = -1, y_ step = 0
            oled.show()
            sleep_ms(12) # sleep for 12 miliseconds

        oled.fill(0) # clear screen


# Constructs a string to display to the screen in format: "mm:ss"
# Input: oled, 2 integers
def displayTimeFormat(oled, minutes, seconds):

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
