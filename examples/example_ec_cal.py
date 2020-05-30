'''Description
Performs a two point calibration. 
Waits for user input before moving on to the next step.
'''

import os
import time
from atlas import AtlasEC

def main():
    ec = AtlasEC() #Create the EC EZO object.
    
    ptype = input('Please enter probe type value (i.e 0.1, 1.0, 10.0).\n')
    ec.probe_type(ptype)

    print('Clearing previous calibration info.')
    ec.cal_clear()
    time.sleep(3)
    
    r1 = input("Please dry the probe for a dry calibration. Once dry, hit enter.\n")
    if r1 == '':
        ec.cal_dry()
        time.sleep(3)
    else:
        print('Dry calibration not performed. Exit script.\n')
        os.exit()
    
    print('Place the probe in a low value solution.\n')
    time.sleep(5)
    
    r2 = input("Please select low value for calibration.\n")
    ec.cal_low(float(r2))
    time.sleep(1)
    
    print("Place the probe in a high value solution.\n")
    time.sleep(5)
    
    r3 = input("Please select high value for calibration.\n")
    ec.cal_high(float(r3))
    time.sleep(1)
    
    ec.cal_status()

    
if __name__ == "__main__":
    main()