# importing the requests library
import urequests
import json

# Returns a tuple:
# - current temperature
# - weather description
def getWeather():

    # api-endpoint
    base_url = "https://api.weather.gov/gridpoints/"

    # location
    gridpoint = "BTV" # use the Burlington station
    longitude = "92"
    latitude = "35"
    special_req = "forecast/hourly/"

    # complete url address
    complete_url = base_url + gridpoint + "/" + longitude + "," + latitude + "/" + special_req

    # send get request and saving the response as response object
    response = urequests.get(complete_url)

    # get data in json format
    #data = response.json()
    print(response.headers())
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
