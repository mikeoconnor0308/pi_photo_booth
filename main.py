import time
import picamera
import RPi.GPIO as GPIO
import atexit
import os
import sys
import pygame
from gamescreen import PhotoboothGame

#######################
### Variables Config ##
#######################

big_button = 5
led = 26
stop_button = 4
focus = 16
shoot = 12

####################
### Other Config ###
####################

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(focus, GPIO.OUT)
GPIO.setup(shoot, GPIO.OUT)
GPIO.setup(big_button, GPIO.IN)
GPIO.setup(stop_button, GPIO.IN)
GPIO.setup(32, GPIO.OUT, initial=False)

camera = picamera.PiCamera()

camera.resolution = (1024, 768)
camera.annotate_text_size = 70
camera.annotate_background = picamera.Color('white')
camera.annotate_foreground = picamera.Color('black')
camera.exposure_compensation = 25

# initialise directory.
photo_dir = "photos"
if not os.path.exists(photo_dir):
    os.makedirs(photo_dir)

game = PhotoboothGame(photo_dir)


def countdown(t):
    i = t
    while i > 0:
        camera.annotate_text = '   5   '
        print('5')
        time.sleep(1)
        i -= 1
    camera.annotate_text = ''


def take_photo():
    now = time.strftime("%Y-%m-%d-%H:%M:%S")
    try:
        GPIO.output(led, 0)
        GPIO.output(focus, 1)
        camera.annotate_text = '   Get ready!   '
        print('Get ready!')
        # TODO ready time
        # countdown(1)
        print('Taking photo')
        camera.annotate_text = ''
        GPIO.output(focus, 0)
        # switch game to not showing anything.
        game.capturing_phase()
        camera.stop_preview()
        GPIO.output(shoot, 1)
        camera.capture("{}/weddingshot.jpg".format(photo_dir))
        time.sleep(1)
        GPIO.output(shoot, 0)

    finally:
        display_photo()


def display_photo():
    try:
        print('Displaying photo')
        game.reviewing_phase()
    except FileNotFoundError:
        print('Could not find photo, going back to preview phase')
        game.previewing_phase()
        camera.start_preview()

    finally:
        GPIO.output(led, 1)


GPIO.output(led, 1)
GPIO.output(32, 0)
print('Running')
camera.start_preview()

while True:

    # TODO wire up button events
    # GPIO.wait_for_edge(big_button, GPIO.RISING)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if event.key == pygame.K_SPACE:
                print("Taking photo!")
                time.sleep(0.2)
                take_photo()
