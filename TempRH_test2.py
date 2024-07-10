import minimalmodbus
import time

# Define the Modbus RTU device parameters
sensor_port = '/dev/ttyUSB0'  # Replace with the actual port where your RS485 converter is connected
baudrate = 9600
parity = 'N'
data_bits = 8
stop_bits = 1
slave_id = 0

# Create a Modbus instrument object
instrument = minimalmodbus.Instrument(sensor_port, slave_id)
instrument.serial.baudrate = baudrate
instrument.serial.parity = parity
instrument.serial.bytesize = data_bits
instrument.serial.stopbits = stop_bits

def read_sensor_data(register_address):
    # Read 1 byte of data from the specified register address
    data = instrument.read_register(register_address, functioncode=3, number_of_decimals=0)
    return data

try:
    while True:
        # Read temperature
        temperature = read_sensor_data(41091)
        
        # Read relative humidity
        humidity = read_sensor_data(41095)
        
        # Read dew point
        dew_point = read_sensor_data(41099)
        
        # Print the sensor data
        print(f"Temperature: {temperature}°C")
        print(f"Relative Humidity: {humidity}%")
        print(f"Dew Point: {dew_point}°C")
        
        # Wait for a moment before reading again (adjust as needed)
        time.sleep(2)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Measurement stopped by the user")
