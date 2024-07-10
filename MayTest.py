from datetime import datetime, timedelta
import time
import csv
import os
import minimalmodbus
from Apogee import Quantum

csv_file = 'experiment_data.csv'
csv_header = ['Timestamp','CO2_OUT','CO2_IN','Temp_OUT','RH_OUT','Dew Point_OUT','Temp_IN','RH_IN','Dew Point_IN','Soil Temp','Vol Water Content','E Conductivity','QUANTUM']

# 設定串口參數
port_CO2_OUT = '/dev/ttyUSB_CO2_OUT'
sensor_address_CO2_OUT = 1

port_CO2_IN = '/dev/ttyUSB_CO2_IN'
sensor_address_CO2_IN = 1

port_TempRH_OUT = '/dev/ttyUSB_TempRH_OUT'
sensor_address_TempRH_OUT = 3

port_TempRH_IN = '/dev/ttyUSB_TempRH_IN'
sensor_address_TempRH_IN = 3

port_Soil = '/dev/ttyUSB_Soil'
sensor_address_Soil = 1

apogee = Quantum()
apogee.connect_to_device()

# 建立串口連接
instrument_CO2_OUT = minimalmodbus.Instrument(port_CO2_OUT, sensor_address_CO2_OUT)
instrument_CO2_OUT.serial.baudrate = 9600
instrument_CO2_OUT.serial.timeout = 1

instrument_CO2_IN = minimalmodbus.Instrument(port_CO2_IN, sensor_address_CO2_IN)
instrument_CO2_IN.serial.baudrate = 9600
instrument_CO2_IN.serial.timeout = 1

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

instrument_Soil = minimalmodbus.Instrument(port_Soil, sensor_address_Soil)
instrument_Soil.serial.baudrate = 9600
instrument_Soil.serial.bytesize = 8
instrument_Soil.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument_Soil.serial.stopbits = 1
instrument_Soil.serial.timeout = 1  # 1 second timeout

# 讀取保持寄存器
CO2_starting_address = 0  # 起始地址
CO2_num_registers = 1  # 要讀取的保持寄存器數量


def record_data():
    # Check if the CSV file exists
    file_exists = os.path.isfile(csv_file)

    # Open CSV file in append or write mode based on file existence
    with open(csv_file, 'a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header only if the file is newly created
        if not file_exists:
            writer.writerow(csv_header)

        try:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            
            value_CO2_OUT = instrument_CO2_OUT.read_registers(CO2_starting_address, CO2_num_registers)
            value_CO2_IN = instrument_CO2_IN.read_registers(CO2_starting_address, CO2_num_registers)
            
            value_TempRH1_OUT = instrument_TempRH_OUT.read_register(0x442, functioncode=3, signed=False) /100 #Temperature
            value_TempRH2_OUT = instrument_TempRH_OUT.read_register(0x446, functioncode=3, signed=False) /100 #Relative Humidity
            value_TempRH3_OUT = instrument_TempRH_OUT.read_register(0x44A, functioncode=3, signed=False) /100 #Dew Point
            
            value_TempRH1_IN = instrument_TempRH_IN.read_register(0x442, functioncode=3, signed=False) /100 #Temperature
            value_TempRH2_IN = instrument_TempRH_IN.read_register(0x446, functioncode=3, signed=False) /100 #Relative Humidity
            value_TempRH3_IN = instrument_TempRH_IN.read_register(0x44A, functioncode=3, signed=False) /100 #Dew Point
            
            value_Soil1 = instrument_Soil.read_register(0x0000, functioncode=3, signed=True) /100 #Soil Temperature
            value_Soil2 = instrument_Soil.read_register(0x0001, functioncode=3, signed=False) /100 #Volumetric Water Content
            value_Soil3 = instrument_Soil.read_register(0x0002, functioncode=3, signed=False) #Electrical Conductivity
            
            value_Apogee = round(apogee.get_micromoles(),4)
                
            print(f"CO2_OUT: {value_CO2_OUT}")
            print(f"CO2_IN: {value_CO2_IN}")
            
            print(f"Temperature_OUT: {value_TempRH1_OUT}°C")
            print(f"Relative Humidity_OUT: {value_TempRH2_OUT}%")
            print(f"Dew Point_OUT: {value_TempRH3_OUT}°C")
            
            print(f"Temperature_IN: {value_TempRH1_IN}°C")
            print(f"Relative Humidity_IN: {value_TempRH2_IN}%")
            print(f"Dew Point_IN: {value_TempRH3_IN}°C")
            
            print(f"Soil Temperature: {value_Soil1}")
            print(f"Volumetric Water Content: {value_Soil2}")
            print(f"Electrical Conductivity: {value_Soil3}")
            
            print(f"Quantum: {value_Apogee}")
            
            data_row = [current_time,value_CO2_OUT[0],value_CO2_IN[0],value_TempRH1_OUT,value_TempRH2_OUT,value_TempRH3_OUT,value_TempRH1_IN,value_TempRH2_IN,value_TempRH3_IN,value_Soil1,value_Soil2,value_Soil3,value_Apogee]
            writer.writerow(data_row)
            print(f"已寫入數據: {data_row}")
            print(f"")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

# Main loop to execute scheduled tasks
while True:
    record_data()
    time.sleep(30)  # Check the schedule every second