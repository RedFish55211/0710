import RPi.GPIO as GPIO
import schedule
import time

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

# Schedule relay activation and deactivation times
for hour in range(6, 18):
    schedule.every().day.at(f"{hour}:00").do(turn_on_relay)
    schedule.every().day.at(f"{hour}:05").do(turn_off_relay)

# Main loop to continuously check the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
