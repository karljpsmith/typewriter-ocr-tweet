# Typewriter Tweeter #
This program enables a typewriter to tweet out the text of the last sentence it typed 
(and, optionally, an image of that sentence). The typewriter has a small camera affixed to it, which 
is controlled by a Raspberry Pi 3B+. The script (which is run on boot by cron) listens for three tweet buttons
and a shutdown button. When one of the tweet buttons is pressed, a picture is taken and uploaded to the 
Google Cloud Vision API, which performs OCR extraction and returns a json blob, which is interpreted by the
Raspberry Pi, reduced to the last sentence (or two, or three), and tweeted out using Twython.

## Raspberry Pi ##
```
ssh pi@[IP address]
```
If ssh isn't working, it's possible the pi has been assigned a new IP. ssh using a LAN cable
```
ssh pi@raspberrypi.local
ifconfig
```

Be careful to always shut down the pi using ```sudo shutdown –h now``` or by pressing 
the fourth button on the breadboard. 
If you don't do this, it will likely
corrupt the SD card and you'll have to install everything again. 

The Raspberry Pi executes pi_boot.sh when it boots up through cron (add ```@reboot /home/pi/pi_boot.sh``` 
to the cron file with the command ```crontab -e```). pi_boot.sh activates a virtual environment and 
runs _main.py there.
I had the permissions drift on me for this - if suddenly pi_boot.sh doesn't work try ```chmod 777 pi_boot.sh```

###Development:
To sync pi_boot:
```
rsync -arv /Users/karlsmith/Desktop/pi_boot.sh pi@raspberrypi.local:/home/pi/
```
```./transfer_to_pi.sh``` is a shell script that updates the python script on the raspberry pi using rsync, then ssh-s in.

If you need to kill the currently running python job:
```ps -ef | grep python```
which will give results like :

user      2430     1  0 Jul03 ?        00:00:01 /usr/bin/python -tt /usr/sbin/yum-updatesd

the second column is the pid. then use the kill command as such :
```kill -9 2430 (i.e. the pid returned)```

###Wifi
To add new wifi configurations on a new network, you'll need to ssh through the 
pi's ethernet port. You can test that the connection is good with ```ping [IP address]``` in the terminal,
and to change the wifi config:
```
ssh pi@raspberrypi.local
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
wpa_cli -i wlan0 reconfigure
```

The python script doesn't delete the files after generating them, so it's a good idea to run the following every once in a while:
```find Desktop/ -name "*.jpg" -type f -exec rm -rf {} \;```
which removes all files with the extension .jpg on the Desktop

###Hardware
I purchased the following hardware:
1) CanaKit Raspberry Pi 3 B+ (B Plus) with Premium Clear Case and 2.5A Power Supply https://www.amazon.com/gp/product/B07BC7BMHY
2) Elegoo EL-CK-002 Electronic Fun Kit Bundle https://www.amazon.com/gp/product/B01ERP6WL4
3) Raspberry Pi Camera Module V2 https://www.amazon.com/gp/product/B01ER2SKFS
4) Samsung 32GB MicroSD https://www.amazon.com/gp/product/B06XWN9Q99
5) iKits Panasonic Battery Power Bank https://www.amazon.com/gp/product/B01EWSREUO
6) 24" Flex Cable for Raspberry Pi Camera https://www.adafruit.com/product/1731

With the help of the Santa Barbara Hackerspace and my girlfriend I 
machined a piece to attach the camera to the typewriter without 
interfering with the typing action. I built a cardboard box to house the breadboard, pi, and battery.  

The Pi uses the GPIOzero library to run the pins/LEDs/buttons
https://gpiozero.readthedocs.io/en/stable/api_input.html
I found the following key helpful for wiring: https://pinout.xyz/ 

## Twitter Authentication ##
There's a multi-step process to getting the proper keys. Run twitter_authentication.py locally and follow the guide here:
https://twython.readthedocs.io/en/latest/usage/starting_out.html#dynamic-function-arguments

## Google API ##
You'll need to generate credentials for your pi to call the google cloud vision API. 
Start here: https://console.cloud.google.com/apis
Click on credentials. I've saved mine as a json blob in a folder (not included in the repo) called /auth

##TODO
1) Substitute textblob's spellchecker for something that is context aware (maybe https://github.com/bakwc/JamSpell)
2) Fix the wifi detection (it registers success on mobile wifi, but can't tweet.)