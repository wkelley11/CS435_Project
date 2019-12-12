# Fridge Magnet: CS435 Embedded Systems Project
by Will Kelley and John Cambefort

\*cheesy voice\* Ever wished you'd had a cool interactive digital fridge?
We're not offering you a fridge, but we can offer you our embedded Fridge Magnet!


### Brief Description

We use the ESP32's wifi connectivity to request data from a few APIs, and display it to the OLED screen:
- Time (Network Time Protocol)
- Value of Google stock (Alphavantage.co)
- Euro to USD conversion rate (Alphavantage.co)
- Weather (Accuweather.com)

Note: these are in part a proof of concept.  You can inspire yourself from our API data-collection scripts to collect data from any API of interest and display it to the board as its own 'screen'.  The ESP32 isn't powerful enough to use a web-scraping tool like BeautifulSoup, which is why we resorted to APIs for this project.


### Project Components

- ESP32 Huzzah Featherwing board
- Adafruit Featherwing OLED
- MicroPython

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


### Brief Documentation of Files

**Main files**:
- `boot.py`: connects to our school wifi.  On launch/reset, the board will automatically run this script.
- `main.py`: uses a state machine to transition between various states or screens when a button is pressed.  An Interrupt Service Routine function will trigger when a button is pressed, setting the corresponding flag to True (e.g. `flagA == True` when button A is pressed).  It is up to you to 'lower' the flags by setting them to `False` where needed.  This logic is useful for our state machine.

**Data files** – these all collect web data to be displayed:
- `get_iomessages.py`: GET request to the Adafruit IO API (MQTT server).
- `get_stocks.py`: GET request to the Alphavantage API to collect both a stock and currency exchange value (e.g. the rate of `EUR` to `USD`).
- `get_time.py`: sets the board's time once on launch by polling from an NTP (Network Time Protocol) server, returns the formatted time in hour and minutes to be displayed.
- `get_weather.py`: GET request to the Accuweather API to get the local time (zip-code).

**Display files** – these handle communication with the OLED:
- `add_ons.py`: perhaps the most useful file for anyone looking to use the OLED, this has a text expansion function, smooth scroll, and display time in "minutes:seconds" format.
- `font_petme128_8x8.py`: this is a Micropython library used to display characters to the board. Each character is 8 bytes, where the first bit in the byte is at the top, and the last is at the bottom (the bytes are ordered vertically on the screen).
- `side_bar.py`: handler script to display simple navigation (up and down arrows).
- `ssd1306.py`: slightly modified (just added a function or two) driver for the SSD1306 OLED screen. The driver is from the MicroPython library: https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py


### Notes & Thanks

If the screen is dark, hit the reset button and wait a few seconds! It should turn on.  Make sure to avoid spam-clicking any buttons – some of the APIs may need a few seconds (the connection might be poor).  Avoid overloading the board.

We would have liked to make it easier for you to load the board with the code by splitting things into a couple directories, but the board didn't cope well with these (ampy returned a `tuple index out of range` error – we're not sure why either).

This project was submitted in the context of a classroom, and you may find our final report summary in the `final-report` folder, from a more in-depth overview of things, to current issues with the project, to a `future-work` wish-list for the project, and more.

Many thanks to the Middlebury College Computer Science department, notably Professor Andrea Vaccari, Adafruit, MicroPython, and Wolf Paulus, for all of the help and resources provided!
