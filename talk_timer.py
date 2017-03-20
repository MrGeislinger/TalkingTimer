import os
import time
import datetime
from Adafruit_LED_Backpack import SevenSegment
import RPi.GPIO as io

# Initialize the button to switch timer on/off
io.setmode(io.BCM)
buzz_pin = 14
reset_pin = 17
bttn_pin = 18
io.setup(bttn_pin, io.IN, pull_up_down=io.PUD_UP)
io.setup(reset_pin, io.IN, pull_up_down=io.PUD_UP)
io.setup(buzz_pin,io.OUT)


segment = SevenSegment.SevenSegment(address=0x70)
# Initialize the display. Must be called once before using the display.
segment.begin()


def buzz_on(bpin=14):
    print("Buzzer on")
    io.output(bpin,io.HIGH)

def buzz_off(bpin=14):
    #io.setmode(io.BCM)
    #io.setwarnings(False)
    #io.setup(bpin,io.OUT)
    print("Buzzer off")
    io.output(bpin,io.LOW)

def buzz(beep_dur=0.4,sleep_dur=0.01,total_dur=5):
    i = 0
    while i < total_dur: 
	i += beep_dur + sleep_dur
	buzz_on()
	time.sleep(beep_dur)
	buzz_off()
	time.sleep(sleep_dur)


#
counter = 0
bttn_pressed = False

# Restart the timer
def restart_timer():
    bttn_pressed = False
    counter = 0


def push_button(bttn):
    return not bttn

def display_clock(use_AM=True):
    now = datetime.datetime.now()
    hour = now.hour
    if use_AM:
        if hour > 12:
            hour -= 12
    minute = now.minute
    second = now.second

    segment.clear()
    # Set hours
    segment.set_digit(0, int(hour / 10))     # Tens
    segment.set_digit(1, hour % 10)          # Ones
    # Set minutes
    segment.set_digit(2, int(minute / 10))   # Tens
    segment.set_digit(3, minute % 10)        # Ones
    # Toggle colon
    segment.set_colon(second % 2)              # Toggle colon at 1Hz


def display_timer(seconds):
    minute = seconds / 60
    seconds %= 60
    # Set minutes
    segment.set_digit(0, int(minute / 10))     # Tens
    segment.set_digit(1, minute % 10)          # Ones
    # Set seconds
    segment.set_digit(2, int(seconds / 10))   # Tens
    segment.set_digit(3, seconds % 10)        # Ones
    # Toggle colon
    segment.set_colon(seconds % 2) # Toggle colon at 1Hz


restart_timer()
time.sleep(2)
#bttn_pressed = push_button(bttn_pressed)
show_timer = True
#bttn_pressed = True
buzzer_on = False

while True:
	
    reset_state = io.input(17)
    input_state = io.input(18)

    if reset_state == False:
        counter = 0
        bttn_pressed = False
        print('Reset the timer')
        segment.clear()
        display_timer(0)
        segment.write_display()
        time.sleep(2)
	buzz_off()

    if input_state == False:
        bttn_pressed = not bttn_pressed
        print('Button Pressed')
	if bttn_pressed:
	    print("Starting buzzer...")
	    buzz_on()
        else:
	    print("Stopping buzzer...")
	    buzz_off()
        time.sleep(0.2)

    # print "counter: %d\nshow_timer: %s\n" %(counter,show_timer)
    # if (counter % 30 == 0):
    #     show_timer = not show_timer
    time.sleep(0.1)
    if bttn_pressed:
        #time.sleep(0.1)
        # Increase the time elapsed
        counter += 1
        if (show_timer):
           segment.clear()
	   print "Counter %d, time %d seconds" %(counter,counter/10)
           display_timer(counter/10)
           segment.write_display()
        else:
           segment.clear()
           display_clock()
           segment.write_display()
