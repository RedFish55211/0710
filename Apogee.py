import time
import csv
import serial
import struct
import time

GET_VOLT = b'\x55!'
READ_CALIBRATION = b'\x83'
SET_CALIBRATION = b'\x84%s%s!'
READ_SERIAL_NUM = b'\x87!'
GET_LOGGING_COUNT = b'\xf3!'
GET_LOGGED_ENTRY = b'\xf2%s!'
ERASE_LOGGED_DATA = b'\xf4!'

class Quantum(object):

    def __init__(self):

        """Initializes class variables, and attempts to connect to device"""

        self.quantum = None

        self.offset = 0.347416

        self.multiplier = 9.31478

        self.connect_to_device()

 

    def connect_to_device(self):

        """This function creates a Serial connection with the defined comport and attempts to read the calibration values"""

        self.port = '/dev/serial/ttyACM0' # you'll have to check your device manager and put the actual com port here

        self.quantum = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)

        

            #self.quantum.write(READ_CALIBRATION)

            #self.multiplier = self.quantum.read(5)[1:]
            #print("mult______:"+str(self.multiplier))

            #self.offset = self.quantum.read(4)
            #This factor need to set up, function dosent reply data.
            #self.multiplier = struct.unpack('<f', self.multiplier)[0]
            #print("multiplier update: "+str(self.multiplier))
            
            #self.offset = struct.unpack('<f', self.offset)[0]

        #except (IOError, struct.error):
                #print("errorrrrrrrr")
                #print (data)
                #self.quantum = None

 

    def get_micromoles(self):

        """This function converts the voltage to micromoles"""

        voltage = self.read_voltage()

        if voltage == 9999:

            # you could raise some sort of Exception here if you wanted to

            return
        self.offset = 0.347416
        self.multiplier = 9.31478
        # this next line converts volts to micromoles
        
        #print(voltage)
        #print(self.offset)
        #print(self.multiplier)
        
        micromoles = ((voltage* 1000) - self.offset) * self.multiplier 
        #print("micromoles: "+str(micromoles))
        if micromoles < 0:

            micromoles = 0

        return micromoles



    def read_voltage(self):

        """This function averages 5 readings over 1 second and returns the result."""

        if self.quantum == None:

            try:
                self.connect_to_device()

            except IOError:

                #print("cant connect to device__")

                return

        # store the responses to average

        response_list = []

        # change to average more or less samples over the given time period

        number_to_average = 5

        # change to shorten or extend the time duration for each measurement

        # be sure to leave as floating point to avoid truncation

        number_of_seconds = 1.0

        for i in range(number_to_average):

            try:

                self.quantum = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)
                
                self.quantum.write(GET_VOLT)

                response = self.quantum.read(5)[1:]
                #print(response)

            except IOError:

                print (data)

                # dummy value to know something went wrong. could raise an

                # exception here alternatively

                return 9999

            else:

                if not response:
                    print("no response")

                    continue

                # if the response is not 4 bytes long, this line will raise

                # an exception

                voltage = struct.unpack('<f', response)[0]

                response_list.append(voltage)

                time.sleep(number_of_seconds/number_to_average)

        if response_list:

            return sum(response_list)/len(response_list)
            

        return 0.0



