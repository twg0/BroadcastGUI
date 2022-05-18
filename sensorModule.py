import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
import datetime as dt

GPIO.setmode(GPIO.BCM)
dht = adafruit_dht.DHT11(board.D6)
GPIO.setup(21, GPIO.IN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def sensor():
    try:
        temperature = dht.temperature
        humidity = dht.humidity
    except RuntimeError as e:
        temperature = 999
        humidity = 999
    gas = GPIO.input(21) # on : 1
    result = [temperature,humidity,gas]
    return result
