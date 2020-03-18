import urequests, json

# Returns last published message in Adafruit IO
def getMQTTMessage():

    base_url = "https://io.adafruit.com/api/v2/jcambefort/feeds"
    feed_key = "stringupload"
    data_request = "data/last"
    AIO_key = AIO_secret

    full_url = base_url + "/" + feed_key + "/" + data_request + "/" + "?x-aio-key=" + AIO_key

    response = urequests.get(full_url)
    data = response.json()

    # If web response is OK
    if(response.status_code == 200):
        str = data.get("value")
        return(str)
    else:
        return("Error")
