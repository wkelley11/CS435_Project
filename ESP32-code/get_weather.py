# importing the requests library
import urequests
import json

# Get the Middlebury weather from the Accuweather API using the postal code
def getWeather():

    # API credentials
    user = "jcambefort"
    api_key = "PiTkuJOebHBDoHPEULaEjEkfMAmBorpI"

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
    print(data)
    # status_path = "https://api.weather.gov/"
    # statusr = urequests.get(status_path)
    # #format and print desired data from json file
    # if():
    #     formated_info = data["periods"]
    #
    #     #get current temp
    #     current_temperature = formated_info["temperature"]
    #     print(current_temperature)

        # #get current pressure
        # current_pressure = formated_info["pressure"]
        #
        # #get current hum
        # current_humidity = formated_info["humidity"]
        #
        # #get summary
        # summary = data["weather"]
        # description = summary[0]["description"]
        #
        # #return weather data: temperature and short weather description (e.g. "sunny")
        # return(str(current_temperature), str(description))

getWeather()
