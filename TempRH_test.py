import minimalmodbus
import time

# Define the Modbus RTU device parameters (adjust as needed)
sensor_port = '/dev/ttyUSB0'  # Replace with the actual port where your RS485 converter is connected
sensor_address = 0  # Modbus address of the sensor (typically 1)
baudrate = 9600
parity = 'N'
data_bits = 8
stop_bits = 1

# Define the Modbus register addresses
TEMPERATURE_REGISTER = 41091
HUMIDITY_REGISTER = 41095
DEW_POINT_REGISTER = 41099

# Create a Modbus instrument object
instrument = minimalmodbus.Instrument(sensor_port, sensor_address)
instrument.serial.baudrate = baudrate
instrument.serial.parity = parity
instrument.serial.bytesize = data_bits
instrument.serial.stopbits = stop_bits

#def query_slave_id():
    # Read the current slave ID from the specified register address using Function Code 3
    # = instrument.read_register(40081, functioncode=3)
    #return slave_id

def read_sensor_data(register_address):
    # Read 1 byte of data from the specified register address
    data = instrument.read_register(register_address, functioncode=3, number_of_decimals=0)
    return data

try:
    
    # Query the updated Slave ID
    #queried_slave_id = query_slave_id()
    #print(f"Updated Slave ID: {queried_slave_id}")
    
    while True:
        # Read temperature
        temperature = read_sensor_data(TEMPERATURE_REGISTER)
        
        # Read relative humidity
        humidity = read_sensor_data(HUMIDITY_REGISTER)
        
        # Read dew point
        dew_point = read_sensor_data(DEW_POINT_REGISTER)
        
        # Print the sensor data
        print(f"Temperature: {temperature}°C")
        print(f"Relative Humidity: {humidity}%")
        print(f"Dew Point: {dew_point}°C")
        
        # Wait for a moment before reading again (adjust as needed)
        time.sleep(2)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Measurement stopped by the user")
