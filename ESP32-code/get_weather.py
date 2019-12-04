# importing the requests library
import urequests
import json

# Get the Middlebury weather from the Accuweather API using the postal code
def getWeather():

    # API credentials
    api_key = "gDHp31aDxUWAjKN7RffVTyuYtfNA3Bj7"

    # API: get hourly weather forecast
    base_url  = "https://dataservice.accuweather.com//forecasts/v1/hourly/1hour/"
    api_r = "?apikey="
    zip_r = "&q="

    # zip code
    zip = "05753"

    # Accuweather location_key
    location_key = "2103_PC"

    # complete url address
    complete_url = base_url + location_key + api_r + api_key

    # send get request and saving the response as response object
    response = urequests.get(complete_url)

    # get data in json format
    data = response.json()

    formated_data = data[0]
    temp_data = formated_data["Temperature"]
    temp = temp_data["Value"]
    description = formated_data["IconPhrase"]

    tuple = str(temp), str(description)
    #print(tuple)

    return tuple
