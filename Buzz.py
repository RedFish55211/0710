import time
import RPi.GPIO as GPIO

def buzz():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    p = GPIO.PWM(12, 50)
    p.start(50)
    
    p.ChangeFrequency(523)
    time.sleep(1)
    p.stop()
    GPIO.cleanup()
    
try:
    while True:
        buzz()
except KeyboardInterrupt:
    print("Program stopped by user")    