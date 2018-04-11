import RPi.GPIO as GPIO
import time
import datetime
import os
import requests
import json
import Adafruit_DHT

EMAIL="###########" #your geeny account
PASSWORD="##########" #your geeny account
SERIAL_NUMBER="NMN001" #chose what ever you like
PIN_NUMBER=11
LED_PIN=13
sensor=Adafruit_DHT.DHT22
pin = 4

def login():
    url = 'http://localhost:9000/api/v1/login'
    payload = json.dumps({'email': EMAIL, 'password': PASSWORD})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=payload, headers=headers)
    return response.text == "success"

def publish(myTopic,value):
    print("publishing message...")
    url = 'http://localhost:9000/api/v1/messages/' + SERIAL_NUMBER
    payload = json.dumps({'msgs': [{"topic": myTopic, 'msg': value}]})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=payload, headers=headers)
    print(myTopic+" - "+value+" - "+response.text)

def pause():
  GPIO.output(LED_PIN, GPIO.HIGH)
  time.sleep(1)
  GPIO.output(LED_PIN, GPIO.LOW)
  time.sleep(1)
  GPIO.output(LED_PIN, GPIO.HIGH)
  time.sleep(1)
  GPIO.output(LED_PIN, GPIO.LOW)

def readDHT():
  temperature, humidity = Adafruit_DHT.read_retry(sensor, pin)

  if humidity is not None and temperature is not None:
      publish("temperature",'{0:0.1f}'.format(temperature))
      publish("humidity",'{0:0.1f}'.format(humidity))
  #else:
   #   print('Failed to get reading. Try again!')

def setup():
  if login():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN_NUMBER, GPIO.IN) # Read output from PIR motion sensor
    GPIO.setup(LED_PIN, GPIO.OUT) # led pin 13
    print("GPIO setup done")
  else:
    raise "error in login"

def run():
  while True:
    readDHT()
    if GPIO.input(PIN_NUMBER):
      while GPIO.input(PIN_NUMBER):
        pass
      publish("event",datetime.datetime.now().strftime("%a, %d %b %Y %T %z"))
    pause()

try:
  setup()
  run()
except KeyboardInterrupt:
  pass
finally:
  print "Exit: Cleanup"
  GPIO.cleanup()