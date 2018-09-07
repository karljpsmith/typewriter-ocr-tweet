import threading
import time
import sys
from subprocess import call
from gpiozero import LED, Button
from picamera import PiCamera

from call_GCV_API import ocr_picture_from_path, interpretResponse, getBoundingBox
from tweet import tweet_with_image
from utils import check_wifi_status, crop

# PIN 18 - blue LED (successful tweet)
# PIN 23 - yellow LED (photo taken - light on camera activation, light off GCV API response received)
# PIN 24 - red LED (internet status - blinks for script running but no internet,
#                   solid for internet connection)
# PIN 27 - Shut Down Button
# PIN 22 - Send Tweet (1 sentence long) Button
# PIN 25 - Send Tweet (2 sentences long) Button
# PIN 17 - Send Tweet (3 sentences long) Button

led_blue = LED(18)
led_yellow = LED(23)
led_red = LED(24)
button_tweet_1 = Button(22)
button_tweet_2 = Button(25)
button_tweet_3 = Button(17)
button_shutdown = Button(27)
filepath = '/home/pi/Desktop/{}.jpg'
croppedfilepath = '/home/pi/Desktop/CROPPED_{}.jpg'


def monitor_wifi_status():
    while True:
        if (check_wifi_status()):
            print('wifi on')
            led_red.on()
            time.sleep(10)
            return
        for x in range(5):
            print('wifi off')
            led_red.on()
            time.sleep(0.4)
            led_red.off()
            time.sleep(0.4)


def shutdown():
    print('waiting for shutdown button')
    button_shutdown.wait_for_press()
    print('shutdown button pressed')
    camera.stop_preview()
    call("sudo shutdown -h now", shell=True)


def process_picture(picture_filepath, btn):

    response = ocr_picture_from_path(picture_filepath)

    text_to_tweet = {
        button_tweet_1: interpretResponse(response, 1),
        button_tweet_2: interpretResponse(response, 2),
        button_tweet_3: interpretResponse(response, 3),
                        }[btn]

    if (text_to_tweet): #returns False if a tweet can't be extracted
        boundingBox = {
            button_tweet_1: getBoundingBox(response, 1),
            button_tweet_2: getBoundingBox(response, 2),
            button_tweet_3: getBoundingBox(response, 3),
        }[btn]

        newFilepath = croppedfilepath.format(str(time.time()))
        crop(picture_filepath, boundingBox, newFilepath)
        tweet_with_image(text_to_tweet, newFilepath)
        led_blue.on()
        time.sleep(1)
        led_blue.off()


def tweet_pressed(btn):
    print('tweet button pressed')
    led_yellow.on()
    picture_filepath = filepath.format(str(time.time()))
    print('camera about to capture')
    camera.capture(picture_filepath)
    print('image successfully captured')
    time.sleep(0.2)
    led_yellow.off()
    threading.Thread(target=process_picture(picture_filepath, btn)).start()


threading.Thread(target=monitor_wifi_status).start()
threading.Thread(target=shutdown).start()
camera = PiCamera()
camera.rotation = 180
camera.start_preview()
print('waiting for button')
for button in (button_tweet_1, button_tweet_2, button_tweet_3):
    button.when_pressed = tweet_pressed



