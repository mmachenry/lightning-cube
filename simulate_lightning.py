# This code is adapted from
# https://oneguyoneblog.com/2017/11/01/lightning-thunder-arduino-halloween-diy/
import random
import time
import pygame

led_pin = 7

flash_count_min = 3
flash_count_max = 15

flash_brightness_min = 10
flash_brightness_max = 255

flash_duration_min = 0.001
flash_duration_max = 0.050

next_flash_delay_min = 0.001
next_flash_delay_max = 0.150

thunder_delay_min = 0.5
thunder_delay_max = 3

thunder_file_min = 1
thunder_file_max = 17

loop_delay_min = 5
loop_delay_max = 30

def lightning_strike():
  flash_count = random.randint(flash_count_min, flash_count_max)

  print ("Flashing. Count = ", flash_count)

  for flash in range(flash_count):
    flash_duration = random.uniform(flash_duration_min, flash_duration_max)
    next_flash_delay = random.uniform(next_flash_delay_min, next_flash_delay_max)
    print ("high") # set pin to brightness with PWM
    time.sleep(flash_duration)
    # set pin low
    print ("low")
    time.sleep(next_flash_delay)

  thunder_delay = random.uniform(thunder_delay_min, thunder_delay_max)
  print("Pausing before playing thunder sound, seconds: ", thunder_delay)
  time.sleep(thunder_delay);

  thunder_file = random.uniform(thunder_file_min, thunder_file_max)
  print("Playing thunder sound, file number: ", thunder_file)
  thunder_sound = pygame.mixer.Sound(str(thunder_file) + ".mp3")
  thunder_sound.play()
  while pygame.mixer.get_busy(): pass
  thunder_sound.stop()

  loop_delay = random.uniform(loop_delay_min, loop_delay_max);
  print("Pausing before next loop, seconds: ", loop_delay)
  time.sleep(loop_delay);

if __name__ == '__main__':
  while True:
    lightning_strike()
