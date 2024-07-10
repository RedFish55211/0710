import RPi.GPIO as GPIO
import schedule
import time
from datetime import datetime, timedelta
from datetime import time as dt_time

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

# Generate time objects for on and off times
working_hours = range(0, 23)
on_times = [dt_time(hour, 52,) for hour in working_hours]
off_times = [dt_time(hour, 53) for hour in working_hours]

# Format time objects as strings in "HH:MM" format
on_times_str = [time.strftime("%H:%M", time.strptime(str(t), "%H:%M:%S")) for t in on_times]
off_times_str = [time.strftime("%H:%M", time.strptime(str(t), "%H:%M:%S")) for t in off_times]

# Schedule the relay actions
for on_time, off_time in zip(on_times_str, off_times_str):
    schedule.every().day.at(on_time).do(turn_on_relay)
    schedule.every().day.at(off_time).do(turn_off_relay)

# Main loop to execute scheduled tasks
try:
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check the schedule every second
        print(datetime.now().time())
    
except KeyboardInterrupt:
    # Clean up GPIO configuration when exiting the script
    GPIO.cleanup()
