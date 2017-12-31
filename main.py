import time
import picamera
import RPi.GPIO as GPIO
import atexit
import os
import sys
import pygame

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
GPIO.setup(led,GPIO.OUT)
GPIO.setup(focus,GPIO.OUT)
GPIO.setup(shoot,GPIO.OUT)
GPIO.setup(big_button,GPIO.IN)
GPIO.setup(stop_button,GPIO.IN)
GPIO.setup(32, GPIO.OUT, initial=False)

camera = picamera.PiCamera()
camera.annotate_text_size = 70
camera.annotate_background = picamera.Color('white')
camera.annotate_foreground = picamera.Color('black')

# initialise directory.
photo_dir = "photos"
if not os.path.exists(photo_dir):
    os.makedirs(photo_dir)


# set up game screen
pygame.init()
screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
black = pygame.Color(0 , 0, 0)

def shut_it_down(channel):
    print('Exiting!')
    camera.stop_preview()
    GPIO.output(led,0)
    GPIO.cleanup()
    camera.close()
    pygame.quit()
    os._exit(0)
    #os.system("sudo halt")


def countdown(time):
    i = time
    while i > 0:
        camera.annotate_text = '   5   '
        print('5')
        time.sleep(1)
        i -=1
    camera.annotate_text = ''


def take_photo():
    now = time.strftime("%Y-%m-%d-%H:%M:%S")
    try:
        GPIO.output(led, 0)
        GPIO.output(focus, 1)
        camera.annotate_text = '   Get ready!   '
        print('Get ready!')
        # TODO ready time
        time.sleep(1)
        # countdown(1)
        print('Taking photo')
        camera.annotate_text = ''
        GPIO.output(focus, 0)
        screen.fill(black)
        pygame.display.update()
        camera.stop_preview()
        GPIO.output(shoot, 1)
        camera.capture("{}/weddingshots-{}.jpg".format(photo_dir, now))
        time.sleep(1)
        GPIO.output(shoot, 0)

    finally:
        display_photo(now)


def display_photo(date):
    try:
        print('Displaying photo')
        img = pygame.image.load("{}/weddingshots-{}.jpg".format(photo_dir, date)).convert()
        screen.blit(img, (0,0))
        pygame.display.update()
        #time.sleep(10)
        #screen.fill(black)
        #pygame.display.update()
        #camera.start_preview()

    except:
        print('Could not find photo')
        screen.fill(black)
        pygame.display.update()
        camera.start_preview()

    finally:
        GPIO.output(led, 1)

GPIO.add_event_detect(stop_button, GPIO.RISING, callback=shut_it_down, bouncetime=300)

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