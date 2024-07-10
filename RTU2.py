import time
import csv
import serial
import minimalmodbus

# 設定串口參數
port = '/dev/ttyACM0'  # 根據您的系統設置正確的串口名稱
baudrate = 9600
timeout = 1

# 建立串口連接
instrument = minimalmodbus.Instrument(port, 1)  # 1 是從站地址，根據您的設備進行設置
instrument.serial.baudrate = baudrate
instrument.serial.timeout = timeout

# CSV 檔案名稱和欄位名稱
csv_file = 'modbus_data_01.csv'
csv_header = ['Timestamp', 'Value']

# 開啟 CSV 檔案，設置寫入模式和寫入器
with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    while True:
        # 讀取保持寄存器
        starting_address = 0  # 起始地址
        num_registers = 4  # 要讀取的保持寄存器數量

        try:
            values = instrument.read_registers(starting_address, num_registers)
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            data_row = [current_time, values[0]]
            writer.writerow(data_row)
            print(f"已寫入數據: {data_row}")
        except Exception as e:
            print(f"讀取失敗: {str(e)}")

        time.sleep(1)  
