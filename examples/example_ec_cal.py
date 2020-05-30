'''Description
Performs a two point calibration. 
Waits for user input before moving on to the next step.
'''


import fcntl
import io
import os
import time
from atlas import AtlasEC

def main():
    ec = AtlasEC() #Create the EC EZO object.
    
    print('Clearing previous calibration info.')
    ec.cal_clear()
    time.sleep(3)
    
    r1 = input("Please dry the probe for a dry calibration. Once dry, hit enter.")
    if r1 == '':
        ec.cal_dry()
        time.sleep(3)
    else:
        print('Dry calibration not performed. Exit script.')
        os.exit()
    
    print('Place the probe in a low value solution.')
    time.sleep(5)
    
    r2 = input("Please select low value for calibration")
    ec.cal_low(float(r2))
    time.sleep(1)
    
    print("Place the probe in a high value solution.")
    time.sleep(5)
    
    r3 = input("Please select high value for calibration.")
    ec.cal_high(float(r3))
    time.sleep(1)
    
    status = ec.cal_status()
    print("Cal Status: {}".format(status))
    
    
    
if __name__ == "__main__":
    main()