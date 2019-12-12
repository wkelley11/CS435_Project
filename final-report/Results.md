Results

The refrigerator magnet has all of the functions we initially hoped it would, but they are not all
implemented in the way we originally intended.  First, we were able to successfully adjust the driver to fit the specifications of our OLED display.  The functions we created allowed us to easily send and display data on the OLED.  Figure 1 demonstrates the text scaling function, which uses pixel manipulation to increase the font size to be more legible.  We use this to make the Current Time screen more legible, as seen in Figure 2.

Figure 1.
![alt-text](https://i.imgur.com/sC2txtU.jpg)

Figure 2.
![alt-text](https://i.imgur.com/XytUTly.jpg)

After creating a way to effectively display text on the board, we then had to gather all of the data
that we wanted to display.  We found that gathering data from APIs was the most straightforward way of collecting real-time data from the web, as the data collection and formatting was handled server-side.  For this reason, we ended up getting a lot of the data we display (i.e. Stock, Currency, Weather) from web APIs.  One thing we were unable to complete was a screen that displayed the upcoming menu at Proctor Dining Hall.  We originally planned to parse through the HTML file for the Middlebury Dining Services website to get the menu.  As we neared the deadline, we decided to focus on other tasks, such as including a messaging service and designing a timer.  We deemed these functions to be more useful and true to the purpose of our device than displaying the Proctor menu.
