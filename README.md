# as_sensors
Python 3 modules for working with Atlas Scientific sensors.


## EC EZO

### Functions
Each function is primarily driven by the write_command or read_response functions. These two functions can be called independently if desired, but the user needs to know the EC EZO command string or the number of returned bytes


#### take_sample()
This function asks the EC EZO to take a sample. Depending on how the user sets up the data output, the return is an array of floats positional to the specified output 
or a single float value.

```
data = take_sample()
```

#### output()
This function will enable the specified data throught he params parameter. The params input must be an array of strings, even if only one value is specied.
Strings can be 'EC', 'TDS', 'S', or 'SG'. The EZO always outputs data in this order, so if you remove 'S' from the output, the order would be 'EC', 'TDS', 'SG'.

```
output(params=['EC','TDS','S','SG']) #Enables the output of all data.
output(params = ['EC']) #Enables the output of EC only.
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

#### 