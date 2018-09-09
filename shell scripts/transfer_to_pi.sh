#!/bin/bash
rsync -arv /Users/karlsmith/PycharmProjects/typewriter-ocr-tweet/ pi@raspberrypi.local:/home/pi/Documents/Python
ssh pi@raspberrypi.local