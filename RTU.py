import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import time
import csv
import serial
import minimalmodbus
import struct
import schedule
import os
from Apogee import *

GPIO.setwarnings(False)
# Set the GPIO mode to BOARD
GPIO.setmode(GPIO.BOARD)

# Define the GPIO pin number to which the relay is connected
relay_pin = 38  # Change this to your actual GPIO pin number

# Set up the GPIO pin as an output
GPIO.setup(relay_pin, GPIO.OUT)

# 設定串口參數
port_CO2 = '/dev/ttyUSB_CO2'  # 根據您的系統設置正確的串口名稱
sensor_address_CO2 = 1 

port_TempRH = '/dev/ttyUSB_TempRH'
sensor_address_TempRH = 3

port_Soil = '/dev/ttyUSB_Soil'
sensor_address_Soil = 1


# 建立串口連接
instrument_CO2 = minimalmodbus.Instrument(port_CO2, sensor_address_CO2)  # 是從站地址，根據您的設備進行設置
instrument_CO2.serial.baudrate = 9600
instrument_CO2.serial.timeout = 1

apogee = Quantum()

instrument_TempRH = minimalmodbus.Instrument(port_TempRH, sensor_address_TempRH)
instrument_TempRH.serial.baudrate = 9600
instrument_TempRH.serial.parity = 'N'
instrument_TempRH.serial.bytesize = 8
instrument_TempRH.serial.stopbits = 1

instrument_Soil = minimalmodbus.Instrument(port_Soil, sensor_address_Soil)
instrument_Soil.serial.baudrate = 9600
instrument_Soil.serial.bytesize = 8
instrument_Soil.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument_Soil.serial.stopbits = 1
instrument_Soil.serial.timeout = 1  # 1 second timeout


# CSV 檔案名稱和欄位名稱
csv_file = 'modbus_data.csv'
csv_header = ['Timestamp','CO2Value','QUANTUM','Temperature','Relative Humidity','Dew Point','Soil Temperature','Volumetric Water Content','Electrical Conductivity']


# Function to turn on the relay
def turn_on_relay():
    GPIO.output(relay_pin, GPIO.HIGH)
    print("Relay is ON")

# Function to turn off the relay
def turn_off_relay():
    GPIO.output(relay_pin, GPIO.LOW)
    print("Relay is OFF")

def record_data():
    # Check if the CSV file exists
    file_exists = os.path.isfile(csv_file)

    # Open CSV file in append or write mode based on file existence
    with open(csv_file, 'a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header only if the file is newly created
        if not file_exists:
            writer.writerow(csv_header)
        
        # 讀取保持寄存器
        starting_address = 0  # 起始地址
        num_registers = 1  # 要讀取的保持寄存器數量
        apogee.connect_to_device()

        try:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            
            values_CO2 = instrument_CO2.read_registers(starting_address, num_registers)
            
            value_Apogee = round(apogee.get_micromoles(),4)
            
            value_TempRH1 = instrument_TempRH.read_register(0x442, functioncode=3, signed=False) /100 #Temperature
            value_TempRH2 = instrument_TempRH.read_register(0x446, functioncode=3, signed=False) /100 #Relative Humidity
            value_TempRH3 = instrument_TempRH.read_register(0x44A, functioncode=3, signed=False) /100 #Dew Point
        
            value_Soil1 = instrument_Soil.read_register(0x0000, functioncode=3, signed=True) /100 #Soil Temperature
            value_Soil2 = instrument_Soil.read_register(0x0001, functioncode=3, signed=False) /100 #Volumetric Water Content
            value_Soil3 = instrument_Soil.read_register(0x0002, functioncode=3, signed=False) #Electrical Conductivity
            
            #print("-----------"+str(apogee.get_micromoles()))
            data_row = [current_time, values_CO2[0],value_Apogee,value_TempRH1,value_TempRH2,value_TempRH3,value_Soil1,value_Soil2,value_Soil3]
            writer.writerow(data_row)
            print(f"已寫入數據: {data_row}")
            
        except Exception as e:
            print(f"Error reading or recording data: {str(e)}")
        except KeyboardInterrupt:
            print("Measurement stopped by user.")

        time.sleep(1)  # Wait for 1 second

# Define the schedule for turning the relay on and off
on_times = ["00:00","00:30","01:00","01:30","02:00","02:30","03:00","03:30","04:00","04:30","05:00","05:30","06:00","06:30","07:00","07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"]
off_times = ["00:05","00:35","01:05","01:35","02:05","02:35","03:05","03:35","04:05","04:35","05:05","05:35","06:05","06:35","07:05","07:35","08:05","08:35","09:05","09:35","10:05","10:35","11:05","11:35","12:05","12:35","13:05","13:35","14:05","14:35","15:05","15:35","16:05","16:35","17:05","17:35","18:05","18:35","19:05","19:35","20:05","20:35","21:05","21:35","22:05","22:35","23:05","23:35"]

#on_times = ["21:48","21:50","21:52","21:54","21:56","21:58"]
#off_times = ["21:49","21:51","21:53","21:55","21:57","21:59"]
# Schedule the relay actions
for on_time, off_time in zip(on_times, off_times):
    schedule.every().day.at(on_time).do(turn_on_relay)
    #schedule.every().day.at(on_time).do(record_data)
    schedule.every().day.at(off_time).do(turn_off_relay)
    #schedule.every().day.at(off_time).do(record_data)    

# Main loop to execute scheduled tasks
while True:
    schedule.run_pending()
    record_data()
    time.sleep(30)  # Check the schedule every second



#SUBSYSTEM=="tty", ATTRS{serial}=="A10MXHVR", SYMLINK+="ttyUSB_CO2_OUT"
#SUBSYSTEM=="tty", ATTRS{serial}=="A10MLX0W", SYMLINK+="ttyUSB_TempRH_OUT"

#SUBSYSTEM=="tty", ATTRS{serial}=="AQ025CRR", SYMLINK+="ttyUSB_CO2_IN"
#SUBSYSTEM=="tty", ATTRS{serial}=="AQ024DUQ", SYMLINK+="ttyUSB_TempRH_IN"
#SUBSYSTEM=="tty", ATTRS{serial}=="A10LSN5O", SYMLINK+="ttyUSB_Soil_IN"