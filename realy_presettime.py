import RPi.GPIO as GPIO
import time
import schedule
from datetime import datetime, timedelta
import minimalmodbus
import os
import csv

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

# Schedule the relay on/off timings
for hour in range(24):
    for minute in [25, 55]:
        schedule_time_on = f"{hour:02d}:{minute:02d}"
        
        # Calculate the off time, rolling over to the next hour if needed
        off_time = datetime.strptime(schedule_time_on, "%H:%M") + timedelta(minutes=5)
        schedule_time_off = off_time.strftime("%H:%M")
        
        schedule.every().day.at(schedule_time_on).do(turn_relay_on)
        schedule.every().day.at(schedule_time_off).do(turn_relay_off)

# Main loop to execute scheduled tasks
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.cleanup()