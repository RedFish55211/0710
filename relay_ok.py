import RPi.GPIO as GPIO
import schedule
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

# Define the schedule for turning the relay on and off
on_times = ["23:01", "23:03", "23:05"]
off_times = ["23:02", "23:04", "23:06"]

# Schedule the relay actions
for on_time, off_time in zip(on_times, off_times):
    schedule.every().day.at(on_time).do(turn_on_relay)
    schedule.every().day.at(off_time).do(turn_off_relay)

# Main loop to execute scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)  # Check the schedule every second