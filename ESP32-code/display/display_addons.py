# Python script to modify the display size of a given line of text.
# An expansion factor of 2 would double the size of the text (4 times as many pixels occupied).

from font_petme128_8x8 import alphabet
from time import sleep, sleep_ms

# Input:
# - oled object
# - message to display
# - factor (int) by which to expand the string
# - x and y top-left start coordinates of 1st char
# - spacing to put between each char
def bigText(oled, message, factor, x_start, y_start, spacing):

    # iterate over each char the string
    x = x_start
    y = y_start
    for char in message:
        asc = ord(char)
        byte = alphabet[asc - 32]
        bigChar(oled, byte, factor, x, y)
        x += (factor * 8)

# Expands the size of a single character by a factor
def bigChar(oled, bits, factor, x, y):

    for i in range(len(bits)): # For every row of bits, in matrix bits
        for b in range(8): # for each bit in a byte
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
