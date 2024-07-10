import RPi.GPIO as GPIO
from datetime import datetime, timedelta, time
import time as sys_time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define the GPIO pin number to which the relay is connected
relay_pin = 38  # Change this to your actual GPIO pin number

# Set up the GPIO pin as an output
GPIO.setup(relay_pin, GPIO.OUT)

'''try:
    while True:
        # Turn the relay on (close the circuit)
        GPIO.output(relay_pin, GPIO.HIGH)
        print("Relay is ON")
        time.sleep(10)  # Relay remains ON for 2 seconds

        # Turn the relay off (open the circuit)
        GPIO.output(relay_pin, GPIO.LOW)
        print("Relay is OFF")
        time.sleep(10)  # Relay remains OFF for 2 seconds

except KeyboardInterrupt:
    # Clean up GPIO configuration when exiting the script
    GPIO.cleanup()'''


# Define the on and off times as datetime objects
on_times = [time(hour, 7, 0, 0) for hour in range(0,23)]

# Main loop to continuously check the time and control the relay
try:
    while True:
        current_time = datetime.now().time() #Get only the time part

        # Check if it's time to turn on the relay
        if current_time in on_times:
            GPIO.output(relay_pin, GPIO.HIGH)
            print("Relay is ON")
            sys_time.sleep(1)  # Check the time every second

        else:
            print("NO")
            #print(datetime.now())
            print(current_time)
            print(datetime.now().time())
            print(on_times)
            sys_time.sleep(1)
            
except KeyboardInterrupt:
    # Clean up GPIO configuration when exiting the script
    GPIO.cleanup()