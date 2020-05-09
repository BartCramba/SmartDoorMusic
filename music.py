import RPi.GPIO as GPIO
import pygame.mixer
import time
import mutagen.mp3

def activeSetup():
        global active
        active = 0
        print("Currently Not Active")

def activeState():
        global active
        if active == 1:
                active = 0
                GPIO.output(7, GPIO.LOW)
                print("Currently Not Active")
        if active == 0:
           print("Activating in 10 seconds")
           for x in range(0,10):
               GPIO.output(7, GPIO.HIGH)
               time.sleep(0.2)
               
               GPIO.output(7, GPIO.LOW)
               time.sleep(0.2)

           active = 1
           GPIO.output(7, GPIO.HIGH)
           print("Currently Active")

        else: return


def watchDoor():
        print("a intrat in functia watchDoor")
        global playing
        playing = False
        while True:
 
              if active == 1 and GPIO.input(15) == 1 and playing == False:
                 playing = True
                 pygame.mixer.music.play()
              if GPIO.input(13) == 1:
                 print("Stop button pressed: Exiting")
                 pygame.mixer.music.stop()
                 break
                 
              if GPIO.input(11) == 1:
                 activeState()
                 time.sleep(0.5)

            

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)

activeSetup()

name = "/home/pi/John Cena - intro.mp3"
mp3 = mutagen.mp3.MP3(name)
pygame.mixer.init(mp3.info.sample_rate, -16, 1, 1024)
pygame.mixer.music.load(name)
pygame.mixer.music.set_volume(1.0)
print("Loaded track - " + str(name))

while True:
    if (GPIO.input(13) == 1):
       print("Stop button pressed: Exiting")
       pygame.mixer.music.stop()
       time.sleep(0.2)
   
    if(GPIO.input(11) == 1):
       activeState()
       time.sleep(0.5)

    if (active == 1):
       watchDoor()

    time.sleep(0.1)

GPIO.cleanup() 
