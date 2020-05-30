'''Description
Example script that showcases commonly used AtlasEC class functions.
'''

import datetime
import pandas as pd
import time
from atlas import AtlasEC



def main(): 
    ec = AtlasEC() #Instantiate the class.
    
    
    #Get device information.
    device,firmware = ec.info()  #Get EZO type and firmware version.
    reason,voltage = ec.status() #Get the reason for restart and voltage at VCC
    
    
    #Set and get device name.
    ec.set_device_name('PiCTD')
    name = ec.get_device_name()
    print(name)
    
    #Showcase LED functions
    ec.led_on() 
    ec.led_find(5)  #Test out the EZO find function for 10 seconds.
    ec.led_off()
    ec.led_status()  #Make sure the LED is off.
    time.sleep(3)
    print('Turning LED on.')
    ec.led_on()
    ec.led_status()
    
    
    #Set and check the temperature compensation setting.
    ec.set_temp_comp(0.00)
    comp = ec.get_temp_comp()
    print(comp)
    
    
    ec.set_temp_comp(25.00)
    comp = ec.get_temp_comp()
    print(comp)
    
    
    #Change output of a sample.
    output = ec.output(['EC','TDS','S','SG'])
    print(output)
    

    #Take a sample once per second for 10 seconds and put it in a data frame. 
    #Time between samples is 0.4 s since it takes ~0.6 s to take a sample.
    data = pd.DataFrame()
    for i in range(10):
        now = datetime.datetime.utcnow()
        sample = ec.take_sample() #Take a reading.
        EC = sample[0]  #Split the array up.
        TDS = sample[1]
        S = sample[2]
        SG = sample[3]
        d = pd.DataFrame(data = {'datetime':[now],
                                 'EC':[EC],
                                 'TDS':[TDS],
                                 'S':[S],
                                 'SG':[SG]})
        data = pd.concat([data,d])  #Concatenate with previous for loop.
        time.sleep(0.4)
    data = data.reset_index(drop=True)
    
    print(data)


if __name__ == "__main__":
    main()
    