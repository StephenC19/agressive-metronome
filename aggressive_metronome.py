import mido
import RPi.GPIO as GPIO
from pathlib import Path
import time
import os

SERVO_PIN_1 = 18
SERVO_PIN_2 = 20
TRIGGER_NOTE = 52

# Metronome flags
def on_beat():
    Path('/tmp/beat.txt').touch()

def off_beat():
    os.remove("/tmp/beat.txt")

def start_counter(bpm, time_length=60):
    count = bpm * (time_length/60)
    for i in range(count):
        on_beat()
        time.sleep(60/bpm)
        off_beat()


speed = input("Enter the metronome speed in bpm")
how_long = input("Enter how long you'd like the metronome to run (in seconds)")

start_counter(speed, how_long)

# Open MIDI device connection
try:
    midi_connection = mido.open_input(MIDI_UNIT)
except:
    print("No MIDI device found. Please make sure a device is connected.")
    exit(1)


for msg in midi_connection:
    if msg.type == "note_on" and msg.note == TRIGGER_NOTE:
        trigger_nerf_gun()


120 = 0.5
