#!/usr/bin/env python3

import random
import time
import pygame
import RPi.GPIO as GPIO
import serial
import threading

storm_intensity = 50

led_pins = [8,10]

flash_count_min = 3
flash_count_max = 15

flash_brightness_min = 10
flash_brightness_max = 100

flash_duration_min = 0.001
flash_duration_max = 0.050

next_flash_delay_min = 0.001
next_flash_delay_max = 0.150

thunder_delay_min = 0.5
thunder_delay_max = 3

thunder_file_min = 1
thunder_file_max = 17

loop_delay_min = 5
loop_delay_max = 15

def main():
  GPIO.setmode(GPIO.BOARD)
  threading.Thread(target=read_serial)
  pwms = []

  for led_pin in led_pins:
    GPIO.setup(led_pin, GPIO.OUT)
    pwm = GPIO.PWM(led_pin, 100)
    pwm.start(0)
    pwms.append(pwm)

  pygame.mixer.init()
  pygame.mixer.music.load("audio/heavy-rain-daniel_simon.mp3")
  pygame.mixer.music.set_volume(0.09)
  pygame.mixer.music.play(loops=-1)

  while True:
    lightning_strike(pwms, tty)

  pwm.stop()
  pygame.mixer.music.stop()
  GPIO.cleanup()

def read_serial():
  tty = serial.Serial("/dev/ttyS0", 9600)
  while True:
    message = tty.readline()
    print (message)

def lightning_strike(pwms):
  flash_count = random.randint(flash_count_min, flash_count_max)

  print ("Flashing. Count = ", flash_count)

  for flash in range(flash_count):
    flash_brightness = random.randint(flash_brightness_min,flash_brightness_max)
    flash_duration = random.uniform(flash_duration_min, flash_duration_max)
    next_flash_delay = random.uniform(next_flash_delay_min,next_flash_delay_max)
    for pwm in pwms:
      pwm.ChangeDutyCycle(flash_brightness)
    time.sleep(flash_duration)
    for pwm in pwms:
      pwm.ChangeDutyCycle(0)
    time.sleep(next_flash_delay)

  thunder_delay = random.uniform(thunder_delay_min, thunder_delay_max)
  print("Pausing before playing thunder sound, seconds: ", thunder_delay)
  time.sleep(thunder_delay);

  thunder_file = random.randint(thunder_file_min, thunder_file_max)
  filename = "audio/" + str(thunder_file).zfill(4) + ".ogg"
  print("Playing thunder sound, file number: ", filename)
  thunder_sound = pygame.mixer.Sound(filename)
  thunder_sound.play()
  #time.sleep(thunder_sound.get_length())
  #thunder_sound.stop()

  loop_delay = random.uniform(loop_delay_min, loop_delay_max);
  print("Pausing before next loop, seconds: ", loop_delay)
  time.sleep(loop_delay);

if __name__ == '__main__':
  main()
