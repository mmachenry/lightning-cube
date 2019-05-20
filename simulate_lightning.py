#!/usr/bin/env python3

import random
import time
import pygame
import RPi.GPIO as GPIO
import serial
import threading

MAX_INTENSITY = 150
MIN_INTENSITY = 10
MID_INTENSITY = (MAX_INTENSITY - MIN_INTENSITY) / 2 + MIN_INTENSITY
storm_intensity = MID_INTENSITY

LED_PINS = [19,21]

heavy_thunder = [
    "heavy-thunder-01.ogg",
    "heavy-thunder-02.ogg",
    "heavy-thunder-03.ogg",
    "heavy-thunder-04.ogg",
    "heavy-thunder-05.ogg",
    "heavy-thunder-06.ogg",
    "heavy-thunder-07.ogg",
    ]

distant_thunder = [
    "distant-thunder-01.ogg",
    "distant-thunder-02.ogg",
    "distant-thunder-03.ogg",
    "distant-thunder-04.ogg",
    "distant-thunder-05.ogg",
    "distant-thunder-06.ogg",
    "distant-thunder-07.ogg",
    "distant-thunder-08.ogg",
    "distant-thunder-09.ogg",
    "distant-thunder-10.ogg",
    "distant-thunder-11.ogg",
    "distant-thunder-12.ogg",
    "distant-thunder-13.ogg",
    "distant-thunder-14.ogg",
    "distant-thunder-15.ogg",
    "distant-thunder-16.ogg",
    "distant-thunder-17.ogg",
    "distant-thunder-18.ogg",
    "distant-thunder-19.ogg",
    ]

rain = [
    "rain-light.ogg",
    "rain-medium.ogg",
    "rain-heavy.ogg",
    ]

def main():
    serial_thread = threading.Thread(target=read_serial)
    serial_thread.start()
    pwms = []

    GPIO.setmode(GPIO.BOARD)
    for led_pin in LED_PINS:
        GPIO.setup(led_pin, GPIO.OUT)
        pwm = GPIO.PWM(led_pin, 100)
        pwm.start(0)
        pwms.append(pwm)

    pygame.mixer.init()
    pygame.mixer.music.load("audio/" + rain[2])
    pygame.mixer.music.play(loops=-1)

    while True:
        print ("Looping with storm_intensity=", storm_intensity)
        thunder_and_lightning(pwms, storm_intensity)
        pause_between(storm_intensity)

def cleanup (pwms):
    for pwm in pwms:
        pwm.stop()
    pygame.mixer.music.stop()
    GPIO.cleanup()

def read_serial():
    global storm_intensity
    tty = serial.Serial("/dev/ttyS0", 9600)
    print ("Reading serial data")
    while True:
        message = tty.readline()
        print (message)
        try:
            value = int(message)
            storm_intensity = value
            print ("storm_intensity set to ", storm_intensity)
        except ValueError as err:
            print (err)
        except:
            print ("Unexpected error")

def thunder_and_lightning (pwms, intensity):
    lightning(pwms, intensity)
    gap = scale_to_intensity(intensity, 10, 0)
    print ("Delaying ", gap, " between light and sound")
    time.sleep(gap)
    thunder(intensity)
 
def lightning(pwms, intensity):
    count = random.randint(1, 7)
    brightness = random_scale_to_intensity(intensity, 20, 95, 10)
    print ("Strike: ", count, " times at ", brightness)

    for flash in range(count):
        duration = random.uniform(0.001, 0.05)
        next_delay = random.uniform(0.001, 0.15)

        for pwm in pwms:
            pwm.ChangeDutyCycle(brightness)
        time.sleep(duration)
        for pwm in pwms:
            pwm.ChangeDutyCycle(0)
        time.sleep(next_delay)

def thunder (intensity):
    filename = "audio/"

    if intensity > MID_INTENSITY:
        filename += random.choice(heavy_thunder)
    else:
        filename += random.choice(distant_thunder)

    sound = pygame.mixer.Sound(filename)
    volume = random_scale_to_intensity(intensity, 0.525, 0.975, 0.05)
    sound.set_volume(volume)
    print ("Playing: ", filename, " at ", volume, " volume")
    sound.play()

def pause_between (intensity):
    time.sleep(random_scale_to_intensity(intensity, 15, 5, 3))

def random_scale_to_intensity(intensity, lower, upper, band):
    mid_range = scale_to_intensity(intensity, lower, upper)
    return random.uniform(mid_range - band/2, mid_range + band/2)
    
def scale_to_intensity(intensity, lower, upper):
    percentage = (intensity-MIN_INTENSITY) / (MAX_INTENSITY-MIN_INTENSITY)
    if upper > lower:
        return (upper-lower) * percentage + lower
    else:
        return (lower-upper) * (1-percentage) + upper

if __name__ == '__main__':
    main()

