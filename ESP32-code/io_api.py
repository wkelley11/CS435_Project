import urequests, json

def getMQTTMessage():

    base_url = "https://io.adafruit.com/api/v2/jcambefort/feeds"
    feed_key = "stringupload"
    data_request = "data/last"
    AIO_key = "2edc7052c6c14d59b4348f933ca58556"

    url = "https://io.adafruit.com/api/v2/jcambefort/feeds/stringupload/data/last?x-aio-key=2edc7052c6c14d59b4348f933ca58556"

    # full_url = base_url + "/" +
    #     feedkey + "/" +
    #     data_request + "/" +
    #     "?x-aio-key=" + AIO_key

    response = urequests.get(url)
    data = response.json()

    if(response.status_code == 200):
        str = data.get("value")
        return(str)
    else:
        return("Error: " + str(response.status_code))
