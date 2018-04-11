# Nano Meet Node

We are going to send data from a sensor node to Geeny. The sensor is a Raspberry Pi Zero W with a DHT22 and PIR connected to.

# Materials
- Geeny enabled* Raspberry Pi Zero W 
- DHT22
- PIR sensor
- resistor, breadboard, led, button, cables

* Geeny Hub SDK installed and running on the Pi

# Circuit
![Fritzing Diagram of the Raspberry Pi with DHT22, PIR and Shutdown button](https://github.com/StefanHermannBerlin/NanoMeetSensorNode/blob/master/assets/nanoMeetSensorNodeCircuit.png)

# Step 1

SSH into an Geeny enabled Raspberry Pi ZERO W

```bash
ssh pi@raspberry.local
```
(Replace the name by the one of your Raspberry Pi if you are using a Diego prepared one: pi@geeny1.local)

The default PW is *raspberry*

## Installing the DHT libraries 
(following this example -> https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit-temperatur-messen-dht11-dht22/)

Install packages for the DHT22:

```bash
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl git
```

then install dht library

```bash
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install
```

# Step 2

* Upload and configure the pir.py to your Raspberry Pi.
* Modify the main.py and set the following variables:

```bash
EMAIL=""
PASSWORD=""
SERIAL_NUMBER=""
```

The `SERIAL_NUMBER` can be obtained by registering a new device through the
`geeny-hub` service running in the Rpi.


1. Log in to the `geeny-hub`.

```bash
curl -H "Content-Type: application/json" -X POST \
  -d '{"email":"<your-user>","password":"<your-password>"}' \
  'http://localhost:9000/api/v1/login'
```

2. Register the thing the instance will use.
Maybe you have to greate your own thing type since the one used in this example is not public.
![Thing Type Structure](https://github.com/StefanHermannBerlin/NanoMeetSensorNode/blob/master/assets/Thing-Type-ID.png)

```bash
  curl -X POST \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -d '{
        "name": "NanoMeetNode001",
        "serial_number": "NMN001",
        "thing_type": "3c165199-2ff6-4c7d-8b49-0557c57050a3"
        }' \
    'http://localhost:9000/api/v1/things' > thing.info
```

# Step 3

Install a shutdown button for the Pi (https://gilyes.com/pi-shutdown-button/)

```bash
git clone https://github.com/gilyes/pi-shutdown
sudo touch /etc/systemd/system/pishutdown.service
sudo nano /etc/systemd/system/pishutdown.service
```
copy&paste this content into the file:

[Service]
ExecStart=/usr/bin/python /home/pi/pi-shutdown/pishutdown.py
WorkingDirectory=/home/pi/pi-shutdown/
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=pishutdown
User=root
Group=root

[Install]
WantedBy=multi-user.target

Then enable the service using:

```bash
sudo systemctl enable pishutdown.service
sudo systemctl start pishutdown.service
```

# Step 4

Creating an autostart
```bash
sudo nano /lib/systemd/system/nanomeet.service
```
copy&paste this content into the file:

[Unit]
Description=NanoMeet autostart service
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python /home/pi/main.py

[Install]
WantedBy=multi-user.target

start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable nanomeet.service
```

check status of systemd script
```bash
sudo systemctl status nanomeet.service
```

# Credits
[George](https://github.com/gilyes) Ilyes for Pi Shutdown
https://tutorials-raspberrypi.de for the DHT22 tutorial