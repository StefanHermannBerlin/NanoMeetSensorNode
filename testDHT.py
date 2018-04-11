import Adafruit_DHT

sensor=Adafruit_DHT.DHT22
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')

    
    
def publishEvent(value):
    print("publishing message...")
    url = 'http://localhost:9000/api/v1/messages/' + SERIAL_NUMBER
    payload = json.dumps({'msgs': [{"topic": "hum", 'msg': value}]})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=payload, headers=headers)
    print(response.text)
    
    
    
print('Temp={0:0.1f}'.format(temperature))
'Humidity={1:0.1f}'.format(humidity)