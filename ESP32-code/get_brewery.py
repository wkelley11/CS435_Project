# Returns a random organic brewery
import urequests, json

def getRandombrewery():
    sandbox_url = "https://sandbox-api.brewerydb.com/v2/"
    api_key = "959d14a52188917ea6b23fea9c5ee309"
    endpoint = "brewery/random"

    full_url = sanbox_url + endpoint + "/?key=" + api_key

    response = urequests.get(full_url)
    jsondata = response.json()

    if(response.status_code == 200):
        data = jsondata.get("data")
        brewery = data.get("name")
        return(str(brewery))
    else:
        return("Error")
