'''Description
A class for the Atlas Scientific EC EZO.

Author: iblack
Date: 2020-05-30
'''


import fcntl
import io
import time

class AtlasEC():
    def __init__(self,bus=1,address = 0x64):
        slave = 0x703
        self._r = io.open("/dev/i2c-{}".format(bus),mode="rb",buffering=0)
        self._w = io.open("/dev/i2c-{}".format(bus),mode="wb",buffering=0)        
        fcntl.ioctl(self._r, slave, address)
        fcntl.ioctl(self._w, slave, address)
    
    
    def write_command(self,command):
        '''Main write command.
        Encodes and writes a string to the EZO.
        Used by other functions to write commands to the EC EZO.
        Can be used independently, but user must know EC EZO command strings.
        
        command -- a string command as found in the EC EZO datasheet.
        '''
        cmd = str.encode(command)
        self._w.write(cmd)
    
    
    def read_response(self,num_bytes=32):
        '''Main read command.
        Decodes and parses a response string from the EC EZO.
        Can be used independently from other functions.
        
        num_bytes -- the number of bytes to read from the EC EZO.
        
        After decoding, "empty" or null bytes are represented by \x00 and 
        are removed in the final output.
        
        The response code from the EC EZO is also given as \x01 
        after decode and is removed.
        
        If the return is \x02, the previously written command was invalid or 
        has a syntax error, so no data is returned.
        '''
        raw = self._r.read(num_bytes)        
        if '\xff' in str(raw):
            print('No data in EZO buffer.')
            return False
        elif '\xfe' in str(raw):
            print('EZO still processing request.')
            return False
        elif '\x02' in str(raw):
            print('Command syntax error.')
            return False
        else:
            response = raw.decode()
            for val in ['\x01','\x00']:
                response = response.replace(val,'')
            return response


    def output(self,params = ['EC','TDS','S','SG']): 
        '''Set the data type output by the EC EZO.
        params -- must be an array of strings, even if only one 
            string is presented.
        
        This function first removes all variables from the output, and
            then only enables values the user specifies.
        
        Finally, the function queries the output parameter and returns the 
            set output to show the user the output has changed. 
        '''
        for p in ['EC','TDS','S','SG']: #Drop all params.
            self.write_command('O,{},0'.format(str(p)))
            time.sleep(0.3)                 
        for param in params: #Only output user selected params.
            self.write_command('O,{},1'.format(str(param)))
            time.sleep(0.3)       
            
        #Check the output.
        self.write_command('O,?')
        time.sleep(0.3)
        check = self.read_response()              
        return check

    
    def take_sample(self):
        '''Take a sample and split output string by the commas.
        Return as an array of floats.
        If the output string only contains one value, return as a 
        single float value.
        '''       
        self.write_command('R')
        time.sleep(0.6) 
        data = self.read_response()
        banana = data.split(',')
        data_array = []
        for val in banana:
            d = float(val)
            data_array.append(d)
        if len(data_array) == 1:
            return data_array[0]
        else:    
            return data_array
        

    def led_off(self):
        self.write_command('L,0')
        time.sleep(0.3)

        
    def led_on(self):
        self.write_command('L,1')
        time.sleep(0.3)
            
        
    def led_status(self):
        self.write_command('L,?')
        time.sleep(0.3)
        data = self.read_response()
        if data == '?L,0':
            print('LED is off.')
            return 0
        elif data == '?L,1':
            print('LED is on.')
            return 1
        else:
            print('Error: Response not recognized.')
            return None


    def led_find(self,num_seconds = 30):
        self.write_command('FIND')
        time.sleep(num_seconds)
        self.led_off()
        self.led_on()

    
    
    def info(self):
        '''Get the device type and firmware version.'''     
        self.write_command('I')
        time.sleep(0.3)
        data = self.read_response()
        banana = data.split(',')
        device = banana[1]
        firmware = banana[2]
        return device, float(firmware)
    
    
    def status(self):
        '''Get the last reason for restart and voltage at VCC.
        The reason for restart is returned as a code, with the complimentary
        reason printed in console.
        '''
        self.write_command('STATUS')
        time.sleep(0.3)
        data = self.read_response()
        banana = data.split(',')
        restart_code = banana[1]
        if restart_code == 'P':
            restart_reason = 'Powered Off'
        elif restart_code == 'S':
            restart_reason = 'Software Reset'
        elif restart_code == 'B':
            restart_reason = 'Brown Out'
        elif restart_code == 'W':
            restart_reason = 'Watchdog'
        elif restart_code == 'U':
            restart_reason = 'Unknown'
        print("Reason for last restart: " + restart_reason)            
        voltage = banana[2]
        return restart_code, float(voltage)
    
    
    def device_sleep(self):
        self.write_command('SLEEP')
    
    
    def change_i2c_address(self,address = 0x64):
        if address >= 1 and address <= 127:
            self.write_command('I2C,{}'.format(address))
            return True
        else:
            print("Invalid address entered.") 
            print("Please use address values between 1-127.")
            return False
        
        
    def factory_reset(self):
        self.write_command('FACTORY')
        print('Calibration reset.')
        print('LED is now on.')
        print('All response codes now enabled.')
        
        
    def switch_to_uart(self,baud = 9600):
        self.write_command('BAUD,{}'.format(int(baud)))
        print("EZO is now in UART mode.")
    
    
    def probe_type(self,n = 1.0):
        self.write_command('K,{}'.format(float(n)))
        time.sleep(0.300)
        self.write_command('K,?')
        time.sleep(0.6)
        data = self.read_response()
        return data


    def get_temp_comp(self):
        self.write_command('T,?')
        time.sleep(0.3)
        data = self.read_response()
        return data        
    
    
    def set_temp_comp(self,n):
        self.write_command('T,{}'.format(float(n)))
        time.sleep(0.3)
    
    
    def protocol_lock_status(self):
        self.write_command('PLOCK,?')
        time.sleep(0.3)
        data = self.read_response()
        return data
    
    
    def protocol_lock(self,enable = False):
        if enable == False:
            self.write_command('PLOCK,0')
        elif enable == True:
            self.write_command('PLOCK,1')
        else:
            print('Protocol lock enable parameter requires True or False.')
            print('Defaulting to PLOCK,0')
            self.write_command('PLOCK,0')


    def set_device_name(self,name):
        self.write_command('NAME,{}'.format(str(name)))
        time.sleep(0.6)
    
    
    def get_device_name(self):
        self.write_command('NAME,?')
        time.sleep(0.6)       
        data = self.read_response()
        banana = data.split(',')
        name = banana[1]
        return name
    
    
    def cal_dry(self):
        self.write_command('CAL,DRY')
        time.sleep(0.6)
    
    
    def cal_single(self,n):
        self.write_command('CAL,{}'.format(float(n)))
        time.sleep(0.6)
 
    
    def cal_low(self,n):
        self.write_command('CAL,LOW,{}'.format(float(n)))
        time.sleep(0.6)
 
    
    def cal_high(self,n):
        self.write_command('CAL,HIGH,{}'.format(float(n)))
        time.sleep(0.6)
 
    
    def cal_clear(self):
        self.write_command('CAL,CLEAR')
        time.sleep(0.3)
    
    
    def cal_status(self):
        self.write_command('CAL,?')
        time.sleep(0.3)
        data = self.read_response()
        if '?CAL,0' in data:
            msg = 'No calibration found on EZO.'
        elif '?CAL,1' in data:
            msg = 'Single point calibration found on EZO.'
        elif '?CAL,2' in data:
            msg = 'Two point calibration found on EZO.'
        else:
            msg = 'Response not recognized.'
        print(msg)
        return msg
    
    

            
    

     
        
#------------------------------Under Development------------------------------#   
    def cal_export(self,file = "EC_EZO_CAL.txt"):
        '''Exports calibration information from the EZO to a text file
        on the Raspberry Pi.
        '''
        self.write_command('EXPORT,?')
        time.sleep(0.6)
        data = self.read_response()
        banana = data.split(',')
        self._num_strings = int(banana[1])
        self._num_bytes = int(banana[2])
    
        self.data_array = []
        for i in range(self._num_strings):
            self.write_command('EXPORT')
            time.sleep(0.6)
            data = self.read_response(120)
            self.data_array.append(data)
        
        check = self._export_checksum()
        
        if check == True:
            f = open(file,'w')
            for cal_str in self.data_array:
                f.write(cal_str + '\n')
            f.close()           
            return self.data_array 
        else:
            print('Calibration values corrupted during export.')
            return False
    
    
    def _export_checksum(self):
        '''Compares number of bytes.
        Takes the number of bytes value given by the 'EXPORT,?' command and
        compares that value to the sum of bytes given by the each line of the
        'EXPORT' command.
        
        If the two values match, then the calibration export was successful.
        '''     
        n_char = 0
        for export_str in self.data_array:
            length = len(export_str)
            n_char = n_char + length
        if n_char == self._num_bytes:
            return True
        else:
            return False
        
        
    def cal_import(self,file = "EC_EZO_CAL.txt"):
        '''Import a calibration file.
        Imports a previous fabricated file from cal_export, 
        or a handcrafted file.
        Files can only have up to 12 characters per line.
        '''      
        f = open(file,'r+')
        data_array = f.readlines()
        f.close()
        for i in range(len(data_array)-1):
            cal_string = data_array[i].replace('\n','')
            self.write_command('IMPORT,{}'.format(cal_string))
            time.sleep(0.6)
            
        return
        
    def response_codes(self,enable = True):
        if enable is True:
            self.write_command('*OK,1')
            time.sleep(0.3)
        elif enable is False:
            self.write_command('*OK,0')
            time.sleep(0.3)
        
        data = self.read_response()
        return data