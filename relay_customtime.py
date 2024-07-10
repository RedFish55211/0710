import RPi.GPIO as GPIO
import time
import schedule
from datetime import datetime
import csv
import os

# Set up GPIO
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BOARD)  # Use board numbering
RELAY_PIN = 38  # GPIO pin where relay is connected
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)

# Log file path
relay_log_file = 'relay_log.csv'

# Ensure the log file exists and write the header if it's a new file
if not os.path.isfile(relay_log_file):
    with open(relay_log_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Event'])

# Function to log relay events
def log_relay_event(event):
    with open(relay_log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), event])

# Function to turn the relay on
def turn_relay_on():
    print(f"Relay ON at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    log_relay_event('ON')

# Function to turn the relay off
def turn_relay_off():
    print(f"Relay OFF at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    GPIO.output(RELAY_PIN, GPIO.LOW)
    log_relay_event('OFF')

# Define the on and off times
on_times = ["14:43","14:45","14:47","14:49","14:51","14:53"]
off_times = ["14:44","14:46","14:48","14:50","14:52","14:54"]

# Schedule the relay on/off timings
for on_time, off_time in zip(on_times, off_times):
    schedule.every().day.at(on_time).do(turn_relay_on)
    schedule.every().day.at(off_time).do(turn_relay_off)

# Main loop to execute scheduled tasks
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.cleanup()
