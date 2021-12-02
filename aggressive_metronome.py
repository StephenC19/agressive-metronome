import os
import mido
import time
import threading
import RPi.GPIO as GPIO
from pathlib import Path
from playsound import playsound
from foam_gun_control import *
import subprocess

RIGHT_SERVO_PIN = 2
LEFT_SERVO_PIN = 17
POWER_SERVO_PIN = 3

metronome_sound_file = "metronome_tick.mp3"

# Metronome
def play_blip_sound():
    playsound(metronome_sound_file)

def calculate_accepted_times(bpm, duration):
    current_time = time.time()
    acceptable_times = []
    count = bpm * (duration/60)
    for i in range(count):
        acceptable_times.append(current_time + (60/bpm))

    return acceptable_times

def in_time(hit_time, accepted_times, threshold):
    shoot = True
    print("Hit time: " + str(hit_time))
    for i in accepted_times:
        if abs(hit_time - i) < threshold:
            print("in time - hit: " + str(hit_time) + ", accepted: " + str(i))
            shoot = False
            break
        # elif i < hit_time:
        #     accepted_times.remove(i)
    return shoot

def start_metronome(bpm, time_length):
    count = bpm * (time_length/60)
    for i in range(count):
        sound_thread = threading.Thread(target=play_blip_sound, args=())
        sound_thread.start()
        time.sleep(60/bpm)

# Choose the correct MIDI device
device_list = mido.get_input_names()
device_choice = input("Select the midi device by inputting the number choice:\n" + str(device_list))
midi_device = device_list[int(device_choice) - 1]


# Open MIDI device connection
try:
    # 'TD-17:TD-17 MIDI 1 20:0'
    midi_connection = mido.open_input(midi_device)
except:
    print("No MIDI device found. Please make sure a device is connected.")
    exit(1)


# Setup Metronome
bpm = input("Enter the metronome speed in bpm")
duration = input("Enter how long you'd like the metronome to run (in seconds)")
print("The motivating metronome will start once you hit the first note. \nGood Luck!")
# 4 count in

accepted_times = calculate_accepted_times(bpm, duration)
print(accepted_times)
threshold = 0.30

try:
    time.sleep(2)
    # Start playing sounds

    # Wait for first hit
    for msg in midi_connection:
        start_metronome(bpm, duration)
        break

    # Start aggressive metronomemetronome
    for msg in midi_connection:
        current_time = time.time()
        if not in_time(current_time, accepted_times, threshold):
            shoot()

except KeyboardInterrupt:
    GPIO.cleanup()
