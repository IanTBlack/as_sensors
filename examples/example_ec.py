'''Description
Example script that showcases AtlasEC class functions.
'''

import datetime
import fcntl
import io
import pandas as pd
import time
from atlas import AtlasEC



def main(): 
    ec = AtlasEC() #Instantiate the class.
    device,firmware = ec.info()  #Get EZO type and firmware version.
    
    #Showcase LED functions
    ec.led_off()
    led_status = ec.led_status()
    ec.led_on()
    
    #Change output when taking a sample.
    output = ec.output(['EC'])
    
    data = []
    for i in range(10):
        now = datetime.datetime.utcnow()
        sample = ec.take_sample() #Take a reading to confirm that there is only one value output.
        d = pd.DataFrame(data = {'datetime':[now],'ec':[sample]})
        data = pd.concat([data,d])
        
        
        data.append(sample)
        time.sleep(1)


if __name__ == "__main__":
    main()
    