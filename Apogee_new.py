import time
import minimalmodbus
from Apogee import Quantum

apogee = Quantum()
apogee.connect_to_device()
    
try:
    while True:
                    
        value_Apogee = round(apogee.get_micromoles(),4)

        print(f"Quantum: {value_Apogee}")

        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("Measurement stopped by user.")
except Exception as e:
    print(f"An error occurred: {str(e)}")