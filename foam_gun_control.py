import RPi.GPIO as GPIO
import time

RIGHT_SERVO_PIN = 2
LEFT_SERVO_PIN = 17
POWER_SERVO_PIN = 3

# Servo control
def setup_servo(pin):
    GPIO.setup(pin, GPIO.OUT)
    return GPIO.PWM(pin, 50)

def set_angle(angle, pin, servo_control):
    duty = angle / 18 + 2
    GPIO.output(pin, True)
    servo_control.ChangeDutyCycle(duty)
    GPIO.output(pin, False)

def safe_angle(servo_control, side):
    left = 54
    right = 160
    if side == 'left':
        set_angle(left, LEFT_SERVO_PIN, servo_control)
    else:
        set_angle(right, RIGHT_SERVO_PIN, servo_control)

def trigger_angle(servo_control, side):
    left = 100
    right = 80
    if side == 'left':
        set_angle(left, LEFT_SERVO_PIN, servo_control)
    else:
        set_angle(right, RIGHT_SERVO_PIN, servo_control)

def turn_on_power(servo_control):
    set_angle(70, POWER_SERVO_PIN, servo_control)

def turn_off_power(servo_control):
    set_angle(90, POWER_SERVO_PIN, servo_control)

def shoot():
    RIGHT_SERVO_PIN = 2
    LEFT_SERVO_PIN = 17
    POWER_SERVO_PIN = 3

    GPIO.setmode(GPIO.BCM)

    # Script start
    l = setup_servo(LEFT_SERVO_PIN)
    r = setup_servo(RIGHT_SERVO_PIN)
    m = setup_servo(POWER_SERVO_PIN)

    l.start(5)
    r.start(10.888)
    m.start(7)

    turn_on_power(m)

    trigger_angle(l, 'left')
    trigger_angle(r, 'right')
    time.sleep(1)

    turn_off_power(m)

    safe_angle(l, 'left')
    safe_angle(r, 'right')
    time.sleep(1)

    l.stop()
    r.stop()
    m.stop()
    GPIO.cleanup()
