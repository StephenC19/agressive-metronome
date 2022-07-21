import os
import mido
import threading
import pygame
import sched
import RPi.GPIO as GPIO
from pathlib import Path
from foam_gun_control import *
from time import sleep, time

RIGHT_SERVO_PIN = 2
LEFT_SERVO_PIN = 17
POWER_SERVO_PIN = 3

metronome_sound_file = "120_metronome.mp3"

def calculate_accepted_times(start_time, bpm, duration):
    acceptable_times = []
    count = float(bpm) * (int(duration)/60)
    # Skip first 4 for count in
    for i in range(1, int(count)):
        time_increment = start_time + (i*(60/int(bpm)))
        acceptable_times.append(time_increment)
    return acceptable_times

def in_time(hit_time, accepted_times, threshold):
    in_time = False
    print("Hit time: " + str(hit_time))
    if float(hit_time) < accepted_times[0] or float(hit_time) > accepted_times[-1]:
        return True
    for i in accepted_times:
        if abs(float(hit_time) - i) < threshold:
            print("in time - hit: " + str(hit_time) + ", accepted: " + str(i))
            in_time = True
            break
        # elif i < hit_time:
        #     accepted_times.remove(i)
    return in_time

# Choose the correct MIDI device
device_list = mido.get_input_names()
device_choice = input("Select the midi device by inputting the number choice:\n" + str(device_list))
midi_device = device_list[int(device_choice) - 1]


# Open MIDI device connection
try:
    midi_connection = mido.open_input(midi_device)
except:
    print("No MIDI device found. Please make sure a device is connected.")
    exit(1)


# User input
bpm = input("Enter the metronome speed in bpm: ")
duration = input("Enter how long you'd like the metronome to run (in seconds): ")
print("The motivating metronome will start once you hit the first note. \nGood Luck!")

# Init audio player
pygame.mixer.init()
pygame.mixer.music.load(metronome_sound_file)
sound_thread = threading.Thread(target=pygame.mixer.music.play(), args=())
scheduler = sched.scheduler(time.time, time.sleep)

# Setup accepted times
start_time = time.time() + 4 # Delay start by 4 seconds
accepted_times = calculate_accepted_times(start_time, bpm, duration)

# Start metronome sound
scheduler.enterabs((start_time - 0.07), 1, sound_thread.start, ())
scheduler.run()

threshold = 0.30

# Start listening to midi input notes
try:
    for msg in midi_connection:
        if msg.note == 36 or msg.note == 38:
            current_time = time.time()
            if not in_time(current_time, accepted_times, threshold):
                print("BANG")

except KeyboardInterrupt:
    GPIO.cleanup()
