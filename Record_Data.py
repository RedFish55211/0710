from datetime import datetime, timedelta
import time
import csv
import minimalmodbus
import os

# CSV 檔案名稱和欄位名稱
csv_file = 'experiment_data.csv'
csv_header = ['Timestamp','CO2_OUT','CO2_IN','Temp_OUT','RH_OUT','Dew Point_OUT','Temp_IN','RH_IN','Dew Point_IN','Soil Temp','Vol Water Content','E Conductivity','QUANTUM']

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
            data_row = [current_time,value_CO2_OUT[0],value_CO2_IN[0],value_TempRH1_OUT,value_TempRH2_OUT,value_TempRH3_OUT,value_TempRH1_IN,value_TempRH2_IN,value_TempRH3_IN,value_Soil1,value_Soil2,value_Soil3,value_Apogee]
            writer.writerow(data_row)
            print(f"已寫入數據: {data_row}")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

# Main loop to execute scheduled tasks
while True:
    record_data()
    time.sleep(30)  # Check the schedule every second

# Define the schedule for turning the relay on and off
#on_times = ["00:00","00:30","01:00","01:30","02:00","02:30","03:00","03:30","04:00","04:30","05:00","05:30","06:00","06:30","07:00","07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"]
#off_times = ["00:05","00:35","01:05","01:35","02:05","02:35","03:05","03:35","04:05","04:35","05:05","05:35","06:05","06:35","07:05","07:35","08:05","08:35","09:05","09:35","10:05","10:35","11:05","11:35","12:05","12:35","13:05","13:35","14:05","14:35","15:05","15:35","16:05","16:35","17:05","17:35","18:05","18:35","19:05","19:35","20:05","20:35","21:05","21:35","22:05","22:35","23:05","23:35"]

#SUBSYSTEM=="tty", ATTRS{serial}=="A10MXHVR", SYMLINK+="ttyUSB_CO2_OUT"
#SUBSYSTEM=="tty", ATTRS{serial}=="A10MLX0W", SYMLINK+="ttyUSB_TempRH_OUT"

#SUBSYSTEM=="tty", ATTRS{serial}=="AQ025CRR", SYMLINK+="ttyUSB_CO2_IN"
#SUBSYSTEM=="tty", ATTRS{serial}=="AQ024DUQ", SYMLINK+="ttyUSB_TempRH_IN"
#SUBSYSTEM=="tty", ATTRS{serial}=="A10LSN5O", SYMLINK+="ttyUSB_Soil"