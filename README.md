# Fridge Magnet: CS435 Embedded Systems Project
by Will Kelley and John Cambefort

### Project Components
- ESP32 Huzzah Featherwing board
- Adafruit Featherwing OLED

### Brief Description

We use the ESP32's wifi connectivity to requests data from a few APIs, and display it to the OLED screen:
- Time (Network Time Protocol)
- Value of Apple stock (Alphavantage.co)
- Euro to USD conversion rate (Alphavantage.co)
- Weather (Accuweather.com)

This data is polled and refreshed in real-time.
When you press the button, the board sends a GET request to the respective API, and displays the data!

Please allow for a few seconds of delay after pressing a button (getting data from the web always takes a sec).

### Navigation of the screen – Try it!
Use buttons A (up) and C (down) to navigate through each of the screens and see the data.  Button B will refresh the data and poll it from the API/Network again for you.

This project is a WIP and we especially want to add the ability for users to upload a message to the board, by using the MQTT Protocol.

Thanks!

Note: if the screen is dark, hit the reset button and wait a few seconds! It should turn on.
