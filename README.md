# Fridge Magnet: CS435 Embedded Systems Project
by Will Kelley and John Cambefort

*cheesy voice* Ever wished you'd had a cool interactive fridge?
We can't offer you a fridge, but we can offer you our embedded Fridge Magnet!

### Brief Description

We use the ESP32's wifi connectivity to request data from a few APIs, and display it to the OLED screen:
- Time (Network Time Protocol)
- Value of Apple stock (Alphavantage.co)
- Euro to USD conversion rate (Alphavantage.co)
- Weather (Accuweather.com)

### Project Components

- ESP32 Huzzah Featherwing board
- Adafruit Featherwing OLED
- MicroPython

Note: make sure to purchase the board/OLED with pins soldered on (unless you want to do that).

### Set-Up

1. Flash MicroPython to your board. We recommend Wolf Paulus' guide: https://wolfpaulus.com/micro-python-esp32/
2. Plug the OLED into the ESP32 (it'll' just stack neatly on top)
3. Modify the boot.py file according to your Wifi settings, to connect it to your router.
4. Using ampy (see Wolf Paulus' guide above), `ampy put` the following onto your ESP32:
  - boot.py
  - main.py
  - display
  - data
5. If you made it here, you're solid! Simply reset your board (un-plug / plug bak in, or press the reset button on the OLED) and after a few seconds, the time should pop up on your screen.
6. Read-on to learn how to navigate the screens.


### Navigation
Use buttons A (up) and C (down) to navigate through each of the screens and see the data.  Button B will refresh the data and poll it from the API/Network again for you.

This project is a WIP and we especially want to add the ability for users to upload a message to the board, by using the MQTT Protocol.

Thanks!

Note: if the screen is dark, hit the reset button and wait a few seconds! It should turn on.
