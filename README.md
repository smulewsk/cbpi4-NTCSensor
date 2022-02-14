# NTCSensor

Plugin for Craftbeerpi 4 to measure temperature from NTC sensor using external ADC. The externel ADC is connected to RPi on the I2C bus.


## Parameter

* Offset - Offset which is added to the received sensor data. Positive and negative values are both allowed
* Rs - Value of the series resistor connected to the thermistor
* Rs connected to - Type of Rs connection (330ohms for 10k thermistor, 3.3Kohms for 100k thermistor)
* Vmax - Voltage max of ADC
* Beta - Beta of thermistor
* Delay - Delay of measurement in secs

## Instalation

sudo pip3 install https://github.com/smulewsk/cbpi4-NTCSensor/archive/main.zip

cbpi add cbpi4-NTCSensor
