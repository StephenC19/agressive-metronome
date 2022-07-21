# Motivational Metronome
Are you having trouble with motivation during your practice routines? It can be hard to power through a practice session listening to a metronome non-stop. With this app you can build and run a metronome that keeps you focused with tough love to keep you playing. Playing out of sync or stopping the metronome will annoy you...in the form of being shot by a foam gun or slapped with a fake hand. Whatever your preference, it's up to you to build anyway. Follow the setup below and run the code!

## Setup

### Components List
* Servo x3
* Frame to hold the servos and the foam gun
* Stand or tripod

### Build
Here's how I've built mine but you can build yours differently as long as the end result is the foam dart gun can be shot automatically.
Here's a schematic of the setup.

![Schematic](servo_schematic.png?raw=true "Servo setup")

Servo 1 (Trigger control 1)
  * Ground wire (brown) - pin 9 (ground)
  * Positive write (red) - pin 4 (5v power)
  * Data wire (orange) - pin 3 (GPIO data)

Servo 2 (Trigger control 2)
  * Ground wire (brown) - pin 6 (ground)
  * Positive write (red) - pin 2 (5v power)
  * Data wire (orange) - pin 11 (GPIO data)

Servo 3 (Dart gun motor)
  * Ground wire (brown) - pin 6 (ground)
  * Positive write (red) - pin 2 (5v power)
  * Data wire (orange) - pin 5 (GPIO data)

### Build
Connect the servo to the GPIO pins as per the diagram below.

## Installation
Install the necessary python packages with `pip3 install -r requirements.txt`

## Run
Run the script using `python3 motivational_metronome.py`
