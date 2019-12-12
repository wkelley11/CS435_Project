Future Work

There are four main things that we would like for our refrigerator magnet in the future:

First, to 3D print a case which would house the device and an external battery.  This would allow us to use it effectively as a magnet.  Currently, we have no way of actually mounting the board on a refrigerator without taping it on.

Second, we hope to change out the Featherwing OLED display with the TFT Featherwing that we have.  This would involve adjusting the driver we are currently using, or converting all of our code to be compatible with the CircuitPython driver for the TFT.  The benefit of this would be both an increase in size to the display, as well as the increased functionality of a touchscreen.  This would allow us to improve on our current interface and add more interactive features to the device.

Third, we would like to change the current messaging function to be more user friendly.  Currently, the user has to log in with Adafruit IO with specific credentials in order to upload a message to the board.  We would like to simplify this process to make it easier to send messages.  

Finally, it would be interesting to connect the Adafruit CircuitPlayground to our ESP32 in order to leverage the numerous peripherals that the CircuitPlayground has.  For instance, we could add a (sound) alarm to the timer function, get in-real-time temperature readings, activate the device with the motion sensor, and much more.
