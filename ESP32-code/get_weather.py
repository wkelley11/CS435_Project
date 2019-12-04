# importing the requests library
import urequests
import json

# Returns a tuple:
# - current temperature
# - weather description
def getWeather():

    # api-endpoint
    base_url = "http://openweathermap.org/data/2.5/weather?"

    # api key
    api_key = "82a228a4c8927ad749cc8022b1695974"

    # location
    location = "Middlebury,us"

    # complete url address
    complete_url = base_url + "/appid=" + api_key + "&q=" + location
    #print(complete_url)

    # send get request and saving the response as response object
    response = urequests.get(complete_url)

    # get data in json format
    data = response.json()
    #print(data)

    #format and print desired data from json file
    if((data["cod"] != "404") and (data["cod"] != "401")):
        formated_info = data["main"]

        #get current temp
        current_temperature = formated_info["temp"]

        #get current pressure
        current_pressure = formated_info["pressure"]

        #get current hum
        current_humidity = formated_info["humidity"]

        #get summary
        summary = data["weather"]
        description = summary[0]["description"]

        #return weather data: temperature and short weather description (e.g. "sunny")
        return(str(current_temperature), str(description))
