# Python script to draw an up arrow and down arrow next to the corresponding
# letter button, to help with device navigation and serve as a menu side bar.

# Handler to call the draw up and down arrow functions.
# This function is called in the main.
def draw_side_bar(oled):
    draw_up_arrow(oled)
    draw_down_arrow(oled)


def draw_up_arrow(oled):
    # Draw up arrow
    oled.text('A', 0, 0)
    arrow_top_x = 16
    arrow_top_y = 0
    arrow_height = 8

    # Draw colon
    oled.vline(arrow_top_x - 6, arrow_top_y + 1, 2, 1)
    oled.vline(arrow_top_x - 6, arrow_top_y + 5, 2, 1)

    # Draw arrow
    oled.vline(arrow_top_x, arrow_top_y, arrow_height, 1)     # draw vertical line of height 10
    oled.line(arrow_top_x, arrow_top_y, 13, 3, 1)             # draw left arrow edge
    oled.line(arrow_top_x, arrow_top_y, 19, 3, 1)             # draw right arrow edge

def draw_down_arrow(oled):

    # Draw up arrow
    oled.text('C', 0, 24)
    arrow_top_x = 16
    arrow_top_y = 22
    arrow_height = 8

    arrow_bottom_x = arrow_top_x
    arrow_bottom_y = arrow_top_y + arrow_height

    # Draw colon
    oled.vline(arrow_top_x - 6, arrow_top_y + 1, 2, 1)
    oled.vline(arrow_top_x - 6, arrow_top_y + 5, 2, 1)

    # Draw arrow
    oled.vline(arrow_top_x, arrow_top_y, arrow_height, 1) # draw vertical line
    oled.line(arrow_bottom_x, arrow_bottom_y, 13, arrow_bottom_y - 3, 1) # draw left arrow edge
    oled.line(arrow_bottom_x, arrow_bottom_y, 19, arrow_bottom_y - 3, 1) # draw right arrow edge
