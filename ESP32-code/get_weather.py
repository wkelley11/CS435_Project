import urequests
import json

# Get the local (Middlebury) weather from the Accuweather API, using the zip code
def getWeather():

    # API credentials
    api_key = "K3rGM32WvHlTIGBm28mtQsBAghcJ6cwQ"

    # API: get hourly weather forecast
    base_url  = "https://dataservice.accuweather.com//forecasts/v1/hourly/1hour/"
    api_r = "?apikey="
    zip_r = "&q="

    # zip code (Middlebury, VT)
    zip = "05753"

    # Accuweather location_key
    location_key = "2103_PC"

    # complete url address
    complete_url = base_url + location_key + api_r + api_key

    # send get request and saving the response as response object
    response = urequests.get(complete_url)

    # get data in json format
    data = response.json()

    if((response.status_code != 200)):
        tuple = ("Error:", "API overused.")
        return tuple
    else:
        formated_data = data[0]
        temp_data = formated_data["Temperature"]
        temp = temp_data["Value"]
        description = formated_data["IconPhrase"]

        tuple = str(temp), str(description)

    return tuple
