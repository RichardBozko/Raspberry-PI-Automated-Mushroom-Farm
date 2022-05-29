import os
import time
import RPi.GPIO as GPIO
from datetime import datetime
import sys
import shutil
import linecache

#Length of activation time
turn_on_time = 30
# Lowest acceptable humidity %
humidity_threshold = 95


# GPIO port setup 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.output (22, False)
GPIO.output (18, False)
GPIO.output (11, False)
GPIO.output (15, False)
GPIO.output (16, False)
GPIO.output (13, False)

# Signals the outlet to turn on
def on():
    GPIO.output (11, True)
    GPIO.output (15, True)
    GPIO.output (16, True)
    GPIO.output (13, True)
    time.sleep(0.1)    
    GPIO.output (22, True)
    time.sleep(0.25)
    GPIO.output (22, False)

# Signals the outlet to turn off
def off():
    GPIO.output (11, True)
    GPIO.output (15, True)
    GPIO.output (16, True)
    GPIO.output (13, False)
    time.sleep(0.1)
    GPIO.output (22, True)
    time.sleep(0.25)
    GPIO.output (22, False)
    time.sleep(0.25)

# in both ^ cases, the sleep times & on/off ports are taken from 
# retailer: https://energenie4u.co.uk/catalogue/product/ENER002-2PI


# Read current values for temperature and humidity
def check_sensor(num):
    with open("/opt/zigbee2mqtt/data/state.json") as f:
        for i, line in enumerate(f):
            if i == num:
                # Get only the humidity value from the file
                hum = line.strip().replace(",","")
                hum = hum.replace('"humidity": ', "")
                return float(hum)


# Turn outlet on.
# Then if that does not go through,try again until you get there 
# and log the failures along the way
def turn_on():
    on()
    while(GPIO.output(13, False)):
        on()
        time.sleep(5)


# Turn outlet off.
# Then if that does not go through, try again until you get there
# and log the failures along the way    
def turn_off():
    off()
    while(GPIO.output(13, True)):
        # Why turn on here? I found that trying to go to the off state 
        # from a failed off state almost never works. This does.
        on() 
        time.sleep(5)
        off()
        

    
def main():
    try:
        # Reboot every 30 cycles. I found that without reboots,
        # the microSDs on RPIs that run a constant program with a lot
        # of R/W operations go bust and get corrupted for some reason.
        reboot_counter, dry_counter = 0, 0
        while(reboot_counter <= 30):
            # Read status file for humidity values 
            hum1 = check_sensor(12)
            hum2 = check_sensor(18)
            # If hum too low turn humidifier on for 30 seconds thrice
            if(hum1 < humidity_threshold or hum2 < humidity_threshold):
                for i in range(3):
                    turn_on()
                    time.sleep(turn_on_time)
                    turn_off()
                    time.sleep(60)
                time.sleep(180)
            reboot_counter += 1
            # Wait until new measurments are in
            while((check_sensor(12) == hum1) and (check_sensor(18) == hum2)):
                dry_counter +=1
                # If no new measurements come for an hour, turn on anyway
                # This way unforeseen technical malfunctions won't result in long dry spells
                if(dry_counter >= 30):
                    turn_on()
                    time.sleep(turn_on_time)
                    turn_off()
                    dry_counter = 0
                time.sleep(120)

    # In case of an error make sure the humidifier is off and reboot
    # os.system('reboot') works just as well, though this approach avoids
    # any permission issues
    finally:
        turn_off()
        GPIO.cleanup()
        os.system("sudo reboot")



main()
