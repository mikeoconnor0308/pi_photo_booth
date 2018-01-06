import time
import picamera
import instagramfilters.instagram_filters
from instagramfilters.instagram_filters.filters import *
import shutil
import inspect
import os
import RPi.GPIO as GPIO
import atexit
import os
import sys
import pygame
from gamescreen import *
import threading

camera = picamera.PiCamera()
camera.resolution = (640, 640)
camera.annotate_text_size = 70
camera.annotate_background = picamera.Color('white')
camera.annotate_foreground = picamera.Color('black')
camera.exposure_compensation = 25

# initialise directory.
photo_dir = "photos"
if not os.path.exists(photo_dir):
    os.makedirs(photo_dir)
filter_dir = os.path.join(photo_dir, "filtered")
if not os.path.exists(filter_dir):
    os.makedirs(filter_dir)

game = PhotoboothGame(photo_dir)
# skip to phase for debugging.
start_phase = GamePhase.REVIEWING
game.switch_to_phase(start_phase)

def countdown(t):
    i = t
    while i > 0:
        camera.annotate_text = '   5   '
        print('5')
        time.sleep(1)
        i -= 1
    camera.annotate_text = ''


def generate_filters():
    # bit of a hack, might be slow. just run all the filters.
    for name, obj in inspect.getmembers(instagramfilters.instagram_filters.filters):
        if inspect.isclass(obj):
            filename = os.path.join("photos", "filtered", name + ".jpg")
            shutil.copyfile("{}/weddingshot.jpg".format(photo_dir), filename)
            f = obj(filename)
            f.apply()


def take_photo():
    now = time.strftime("%Y-%m-%d-%H:%M:%S")
    try:
        camera.annotate_text = '   Get ready!   '
        print('Get ready!')
        # TODO ready time
        # countdown(1)
        print('Taking photo')
        camera.annotate_text = ''
        # switch game to not showing anything.
        game.capturing_phase()
        camera.stop_preview()
        camera.capture("{}/weddingshot.jpg".format(photo_dir))
        time.sleep(1)

    finally:
        display_photo()
        # generate filters
        print('Generating filters')
        generate_filters()
        print('Done generating filters')


def display_photo():
    try:
        print('Displaying photo')
        game.reviewing_phase()
    except FileNotFoundError:
        print('Could not find photo, going back to preview phase')
        game.previewing_phase()
        camera.start_preview()


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

            if game.phase == GamePhase.PREVIEWING:
                if event.key == pygame.K_SPACE:
                    print("Taking photo!")
                    time.sleep(0.2)
                    take_photo()
            elif game.phase == GamePhase.REVIEWING:
                if event.key == pygame.K_SPACE:
                    print("Moving to filter screen!")
                    game.filter_phase()
                if event.key == pygame.K_BACKSPACE:
                    print("Back to preview")
                    game.previewing_phase()

