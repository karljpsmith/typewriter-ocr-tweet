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

To sync pi_boot:
```
rsync -arv /Users/karlsmith/Desktop/pi_boot.sh pi@raspberrypi.local:/home/pi/
```
Development:
```./transfer_to_pi.sh``` is a shell script that updates the python script on the raspberry pi using rsync, then ssh-s in.

If you need to kill the currently running python job:
```ps -ef | grep python```
which will give results like :

user      2430     1  0 Jul03 ?        00:00:01 /usr/bin/python -tt /usr/sbin/yum-updatesd

the second column is the pid. then use the kill command as such :
```kill -9 2430 (i.e. the pid returned)```

To add new wifi configurations on a new network, you'll need to ssh through the 
pi's ethernet port. You can test that the connection is good with ```ping raspberrypi.local``` in the terminal,
and to change the wifi config:
```
ssh pi@raspberrypi.local
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
wpa_cli -i wlan0 reconfigure
```

## Twitter Authentication ##

## Google API ##

##TODO
1) Substitute textblob's crappy spellchecker for something that is context aware (maybe https://github.com/bakwc/JamSpell)
2) Use the old camera box for the guts of the detector
3) Fix the wifi detection (it registers success on mobile wifi, but can't tweet.)