# as_sensors
A Python 3 module for working with the Atlas Scientific EC EZO attached to a Raspberry Pi.


## EC EZO

### Functions
Each function is primarily driven by the write_command or read_response functions. These two functions can be called independently if desired, but the user needs to know the EC EZO command string or the number of returned bytes


#### take_sample()
This function asks the EC EZO to take a sample. Depending on how the user sets up the data output, the return is an array of floats positional to the specified output 
or a single float value.

```
data = take_sample()
```

#### output(params)
This function will enable the specified data throught he params parameter. The params input must be an array of strings, even if only one value is specied.
Strings can be 'EC', 'TDS', 'S', or 'SG'. The EZO always outputs data in this order, so if you remove 'S' from the output, the order would be 'EC', 'TDS', 'SG'.

```
output(params=['EC','TDS','S','SG']) #Enables the output of all data.
output(params = ['EC']) #Enables the output of EC only.
```

#### led_off(), led_on()
These functions can be used to power on or off the EZO LED.

#### led_status()
This function queries the LED status, it returns 0 if the LED is off and 1 if the LED is on.

#### led_find(num_seconds)
This function will flash the LED for specified number of seconds.

```
led_find(10)  #Flashes the LED for 10 seconds.
```


#### info()
Returns the device type and firmware number.
```
device,firmware = info()
```

#### status()
Returns the last reason for device restart and the voltage at the EC EZO VCC pin.

```
reason,voltage = status()
```

#### device_sleep()
Puts the EC EZO to sleep. Any subsequent command wakes up the EZO.

#### change_i2c_address(address)
Changes the I2C address of the EC EZO. If the value is outside of 1-127, False is returned. 
Changing the address requires specification of the address in AtlasEC() in subsequent calls.

#### factory_reset()
Resets the EZO to factory settings. This resets the calibration, turns the LED on, and enables all response codes.

#### switch_to_uart(baud)
Puts the EZO in UART mode at a specified baud rate.

#### probe_type(n)
Tells the EC EZO the attached probe type. Common options would be 0.1, 1.0, or 10.0.

#### get_temp_comp()
Gets the current temperature compensation setting of the EZO.

#### set_temp_comp(n)
Sets the temperautre compensation of the EZO. Value must be in degC.

#### protocol_lock_status()
Asks the EC EZO if the current communication protocol is locked.

#### protocol_lock(enable)
If enable is True, the EZO locks the current communcation protocol.

If enable is False, the EZO does not lock the current communication protocol. 
By default, this command unlocks the communication protocol.

#### set_device_name(name)
Sets a custom name for the EZO. Must be formatted as a string.

#### get_device_name()
Gets the name of the EZO.

#### cal_dry()
Performs a dry calibration of the attached probe.

#### cal_single(n)
Performs a single point calibration while the probe is in the reference solution of value n.

#### cal_low(n)
Performs a low calibration for a two point calibration while the probe is in a reference solution of value n.

#### cal_high(n)
Performs a high calibration for a two point calibration while the probe is in a reference solution of value n.

#### cal_clear()
Clear the previous calibration from the EC EZO.

#### cal_status()
Check the calibration type of the EZO. Returns either one-point, two-point, or no calibration.



