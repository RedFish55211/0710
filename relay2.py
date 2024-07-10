import RPi.GPIO as GPIO
from datetime import datetime, timedelta, time
import time

GPIO.setwarnings(False)

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BOARD)

# Define the GPIO pin number to which the relay is connected
relay_pin = 38  # Change this to your actual GPIO pin number

# Set up the GPIO pin as an output
GPIO.setup(relay_pin, GPIO.OUT)

# Function to turn on the relay
def turn_on_relay():
    GPIO.output(relay_pin, GPIO.HIGH)
    print("Relay is ON")

# Function to turn off the relay
def turn_off_relay():
    GPIO.output(relay_pin, GPIO.LOW)
    print("Relay is OFF")

# Define the on and off times as datetime objects
on_times = [datetime.strptime(f"{hour}:48:00", "%H:%M:%S") for hour in range(6, 23)]
off_times = [datetime.strptime(f"{hour}:49:00", "%H:%M:%S") for hour in range(6, 23)]

# Main loop to continuously check the time and control the relay

try:
    while True:
        current_time = datetime.now()

        # Check if it's time to turn on the relay
        if current_time in on_times:
            turn_on_relay()

        # Check if it's time to turn off the relay
        if current_time in off_times:
            turn_off_relay()

        time.sleep(1)  # Check the time every second

except KeyboardInterrupt:
    # Clean up GPIO configuration when exiting the script
    GPIO.cleanup()
    
    
    
    
    
