import minimalmodbus
import time

port_TempRH_OUT = '/dev/ttyUSB_TempRH_OUT'
sensor_address_TempRH_OUT = 3

port_TempRH_IN = '/dev/ttyUSB_TempRH_IN'
sensor_address_TempRH_IN = 3

# Create a Modbus instrument object
instrument_TempRH_OUT = minimalmodbus.Instrument(port_TempRH_OUT, sensor_address_TempRH_OUT)
instrument_TempRH_OUT.serial.baudrate = 9600
instrument_TempRH_OUT.serial.parity = 'N'
instrument_TempRH_OUT.serial.bytesize = 8
instrument_TempRH_OUT.serial.stopbits = 1

instrument_TempRH_IN = minimalmodbus.Instrument(port_TempRH_IN, sensor_address_TempRH_IN)
instrument_TempRH_IN.serial.baudrate = 9600
instrument_TempRH_IN.serial.parity = 'N'
instrument_TempRH_IN.serial.bytesize = 8
instrument_TempRH_IN.serial.stopbits = 1


try:
    while True:
        
        value_TempRH1_OUT = instrument_TempRH_OUT.read_register(0x442, functioncode=3, signed=False) /100 #Temperature
        value_TempRH2_OUT = instrument_TempRH_OUT.read_register(0x446, functioncode=3, signed=False) /100 #Relative Humidity
        value_TempRH3_OUT = instrument_TempRH_OUT.read_register(0x44A, functioncode=3, signed=False) /100 #Dew Point
        
        value_TempRH1_IN = instrument_TempRH_IN.read_register(0x442, functioncode=3, signed=False) /100 #Temperature
        value_TempRH2_IN = instrument_TempRH_IN.read_register(0x446, functioncode=3, signed=False) /100 #Relative Humidity
        value_TempRH3_IN = instrument_TempRH_IN.read_register(0x44A, functioncode=3, signed=False) /100 #Dew Point
    
        # Print the sensor data
        print(f"Temperature_OUT: {value_TempRH1_OUT}°C")
        print(f"Relative Humidity_OUT: {value_TempRH2_OUT}%")
        print(f"Dew Point_OUT: {value_TempRH3_OUT}°C")
        
        print(f"Temperature_IN: {value_TempRH1_IN}°C")
        print(f"Relative Humidity_IN: {value_TempRH2_IN}%")
        print(f"Dew Point_IN: {value_TempRH3_IN}°C")
        
        # Wait for a moment before reading again (adjust as needed)
        time.sleep(2)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Measurement stopped by the user")