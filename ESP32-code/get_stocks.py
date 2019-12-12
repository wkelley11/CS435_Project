# Use Alphavantage.co to get financial information

import urequests
import json
from utime import localtime

# Returns current
def getStocks(stock):
    # Alphavantage credentials
    api_key = "NRKWC04SMTNZ17H2"

    # Alphavantage API request url
    base_url = "https://www.alphavantage.co/query?"

    function = "function=TIME_SERIES_DAILY"
    symbol = "symbol=" + stock # get the current stock value

    complete_url = base_url + function + "&" + symbol + "&apikey=" + api_key

    response = urequests.get(complete_url)

    data = response.json()

    if(response.status_code != "404"):

        (year, month, day, hour, minute, second, weekday, yearday) = localtime()

        times = data["Time Series (Daily)"]

        try:
            todayDate = str(year) + "-" + str(month) + "-" + str(day)

            todayValues = times[str(todayDate)]

            current_value = todayValues.get("4. close")

            return current_value

        except KeyError:
            try:
                todayDate = str(year) + "-" + str(month) + "-" + str(day - 1)
                todayValues = times[str(todayDate)]
                current_value = todayValues.get("4. close")
                return current_value
            except KeyError:
                return("Stocks: Error!")

    else:
        return("Stocks: Error!")

# Returns current from_currency to to_currency conversion rate
def getExchange(from_currency, to_currency):

    # Alphavantage credentials
    api_key = "NRKWC04SMTNZ17H2"

    # Alphavantage API request url
    base_url = "https://www.alphavantage.co/query?"

    function = "function=CURRENCY_EXCHANGE_RATE"
    from_c = "from_currency=" + from_currency
    to_c = "to_currency=" + to_currency

    complete_url = base_url + function + "&" + from_c + "&" + to_c + "&apikey=" + api_key

    response = urequests.get(complete_url)

    data = response.json()

    all = data.get("Realtime Currency Exchange Rate")

    er = all.get("5. Exchange Rate")

    return er
