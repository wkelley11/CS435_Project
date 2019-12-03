# Python script to modify the display size of a given line of text.
# An expansion factor of 2 would double the size of the text (4 times as many pixels occupied).

def bigText(oled, bits, factor, x, y):

    for i in range(len(bits)): # For every row of bits, in matrix bits
        for b in range(8): # for each bit in a byte
            for row in range(factor):
                for col in range(factor):
                    oled.pixel((factor * i) + row + x, (factor * b) + col + y, bits[i]&(0x01<<b))
