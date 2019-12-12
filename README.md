# Fridge Magnet: CS435 Embedded Systems Project
by Will Kelley and John Cambefort

\*cheesy voice\* Ever wished you'd had a cool interactive digital fridge?
We're not offering you a fridge, but we can offer you our embedded Fridge Magnet!

### Project Components

- ESP32 Huzzah Featherwing board
- Adafruit Featherwing OLED
- MicroPython

### Brief Description

We use the ESP32's wifi connectivity to request data from a few APIs, and display it to the OLED screen:
- Time (Network Time Protocol)
- Value of Apple stock (Alphavantage.co)
- Euro to USD conversion rate (Alphavantage.co)
- Weather (Accuweather.com)

Note: make sure to purchase the board/OLED with pins soldered on (unless you want to do that).

### Set-Up

1. Flash MicroPython to your board. We recommend Wolf Paulus' guide: https://wolfpaulus.com/micro-python-esp32/
2. Plug the OLED into the ESP32 (it'll' just stack neatly on top)
3. Modify the boot.py file according to your Wifi settings, to connect it to your router.
4. Using `ampy` (see Wolf Paulus' guide above), `ampy put` all of the files in the `ESP32-Code` directory onto the ESP32.
5. If you made it here, you're solid! Simply reset your board (un-plug / plug bak in, or press the reset button on the OLED) and after a few seconds, the time should pop up on your screen.
6. Read-on to learn how to navigate the screens.

### Navigation

- Use buttons A (up) and C (down) to navigate through each of the screens and view the data.
- If you're on the Timer screen:
  - A will increment 1 to the Timer.
  - B will let you enter the Timer function, start the timer once you've set it, and pause & resume the countdown.
  - C will let you exit the Timer.

### Using MQTT to Upload Messages

You can send data from your phone to the screen with the MQTT protocol.  Here's how:

- Download any MQTT phone app, and add the connection with the following credentials:
  - Name: anything you want to name this (it'll only show up in your app)
  - Address: `io.adafruit.com`
  - Port: `1883`
  - User name: `jcambefort` (you're welcome to make your own account!)
  - User password: `2edc7052c6c14d59b4348f933ca58556` (known as your "AIO key" on Adafruit IO)
  - Client ID: the name you want your device to be recognized as by the Adafruit IO server
- Add a `text` or `string` block to your app dashboard (and/or Adafruit IO dashboard)
- Type away!  When you access the MQTT screen (between the Timer and the Weather screens), the message should display.  If longer than 15 characters, the message will scroll across the screen.

### Notes & Thanks

If the screen is dark, hit the reset button and wait a few seconds! It should turn on.  Make sure to avoid spam-clicking any buttons – some of the APIs may need a few seconds (the connection might be poor).  Avoid overloading the board.

We would have liked to make it easier for you to load the board with the code by splitting things into a couple directories, but the board didn't cope well with these (ampy returned a `tuple index out of range` error – we're not sure why either).

This project was submitted in the context of a classroom, and you may find our final report summary in the `final-report` folder, from a more in-depth overview of things, to current issues with the project, to a `future-work` wish-list for the project, and more.

Many thanks to the Middlebury College Computer Science department, notably Professor Andrea Vaccari, Adafruit, MicroPython, and Wolf Paulus, for all of the help and resources provided!
