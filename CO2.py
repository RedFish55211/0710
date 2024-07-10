import time
import minimalmodbus


# 設定串口參數
port_CO2_OUT = '/dev/ttyUSB_CO2_OUT'
sensor_address_CO2_OUT = 1

port_CO2_IN = '/dev/ttyUSB_CO2_IN'
sensor_address_CO2_IN = 1


# 建立串口連接
instrument_CO2_OUT = minimalmodbus.Instrument(port_CO2_OUT, sensor_address_CO2_OUT)
instrument_CO2_OUT.serial.baudrate = 9600
instrument_CO2_OUT.serial.timeout = 1

instrument_CO2_IN = minimalmodbus.Instrument(port_CO2_IN, sensor_address_CO2_IN)
instrument_CO2_IN.serial.baudrate = 9600
instrument_CO2_IN.serial.timeout = 1

# 讀取保持寄存器
CO2_starting_address = 0  # 起始地址
CO2_num_registers = 1  # 要讀取的保持寄存器數量

try:
    while True:
                    
        value_CO2_OUT = instrument_CO2_OUT.read_registers(CO2_starting_address, CO2_num_registers)
        value_CO2_IN = instrument_CO2_IN.read_registers(CO2_starting_address, CO2_num_registers)
            
        print(f"CO2_OUT: {value_CO2_OUT}")
        print(f"CO2_IN: {value_CO2_IN}")

        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("Measurement stopped by user.")
except Exception as e:
    print(f"An error occurred: {str(e)}")