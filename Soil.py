import minimalmodbus
import time

# Define the Modbus slave address and port (typically /dev/ttyUSB0 or similar)
port_Soil = '/dev/ttyUSB_Soil'
sensor_address_Soil = 1

# Create a Modbus instrument object
instrument_Soil = minimalmodbus.Instrument(port_Soil, sensor_address_Soil)

# Configure the instrument
instrument_Soil.serial.baudrate = 9600
instrument_Soil.serial.bytesize = 8
instrument_Soil.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument_Soil.serial.stopbits = 1
instrument_Soil.serial.timeout = 1  # 1 second timeout

try:
    while True:
        
        value_Soil1 = instrument_Soil.read_register(0x0000, functioncode=3, signed=True) /100 #Soil Temperature
        value_Soil2 = instrument_Soil.read_register(0x0001, functioncode=3, signed=False) /100 #Volumetric Water Content
        value_Soil3 = instrument_Soil.read_register(0x0002, functioncode=3, signed=False) #Electrical Conductivity
        
        print(f"Soil Temperature: {value_Soil1}")
        print(f"Volumetric Water Content: {value_Soil2}")
        print(f"Electrical Conductivity: {value_Soil3}")
        
        # Wait for a moment before reading again (adjust as needed)
        time.sleep(2)
            
except KeyboardInterrupt:
    print("Measurement stopped by user.")
except Exception as e:
    print(f"An error occurred: {str(e)}")