# 30 requests per minute on Adafruit IO

import umqtt.simple as mqtt
import utime

client_id = "my_esp32_hehe"
broker_address = "io.adafruit.com"
AIO_USER = "jcambefort"
AIO_KEY = "2edc7052c6c14d59b4348f933ca58556"
feed = "jcambefort/feeds/stringupload"
ioadafruit_secure_port = 1883 # public port is 1883

#def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=0,
                 #ssl=False, ssl_params={}):

c = mqtt.MQTTClient(client_id, broker_address, port=ioadafruit_secure_port, user=AIO_USER, password=AIO_KEY)

# Global variables
fromio = ""  # Initialize to empty: stores message
new_msg = False

def callbackme(topic, msg):

    global fromio, new_msg

    new_msg = True # we've received a new message

    bytes = msg
    out = bytes.decode("utf-8")
    fromio = out


c.set_callback(callbackme)
c.connect()
c.subscribe(feed)

c.check_msg()

utime.sleep(2)
