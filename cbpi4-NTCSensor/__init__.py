
# -*- coding: utf-8 -*-
import os
import logging
import asyncio
from cbpi.api import *
from math import log

import smbus

i2c_channel = 1

MCP3421_I2C_ADDRESS = 0x68
RAW_TO_V_FACTOR = 0.000015625
MCP3421_CONFIG_BYTE = 0x1c

T0_25C = 298.15

def getSensors():
    return ["Thermistor100k","Thermistor10k"]

logger = logging.getLogger(__name__)

@parameters([Property.Select("Sensor", getSensors(), description="The NTC sensor type."),
    Property.Number(label="Offset", configurable=True, default_value=0, description="Offset which is added to the received sensor data. Positive and negative values are both allowed."),
    Property.Number("Rs", True, 3300, description="Value of the series resistor connected to the thermistor."),
    Property.Select("Rs connected to", ["5V", "GND"], description="Type of Rs connection."),
    Property.Number("Vmax", True, 5, description="Voltage max of ADC."),
    Property.Number("Beta", True, 3950, description="Beta of thermistor."),
    Property.Number("Delay", True, 1, description="Delay of measurement in secs.")])
class NTCSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(NTCSensor, self).__init__(cbpi, id, props)
        self.bus = smbus.SMBus(i2c_channel)
        self.bus.write_byte(MCP3421_I2C_ADDRESS, MCP3421_CONFIG_BYTE)
        self.value = 0

    def get_adc_measure(self):
        self.mcpdata = self.bus.read_i2c_block_data(MCP3421_I2C_ADDRESS, MCP3421_CONFIG_BYTE,4)
        return (self.mcpdata[2] + (self.mcpdata[1] << 8) + (self.mcpdata[0] << 16)) * RAW_TO_V_FACTOR

    async def start(self):
        await super().start()
        self.running = True
        self.sensor_name = self.props.get("Sensor")
        self.offset = float(self.props.get("Offset", 0))
        self.rs = float(self.props.get("Rs", 3300))
        self.rs_connection = self.props.get("Rs connected to")
        self.adcMax = float(self.props.get("Vmax", 5))
        self.beta = float(self.props.get("Beta", 3950))
        self.delay = float(self.props.get("Delay", 1))

    async def stop(self):
        try:
            self.running = False
        except:
            pass

    async def run(self):
        while self.running is True:
            T=0
            adcVal = self.get_adc_measure()

            if adcVal > self.adcMax:
                adcVal = self.adcMax

            if adcVal != 0:
                if self.sensor_name == "Thermistor100k":
                    r0 = 100000.0
                elif self.sensor_name == "Thermistor10k":
                    r0 = 10000.0
                else:
                    r0 = 100000.0

                if self.rs_connection == "GND":
                    rt = self.rs * ((self.adcMax/adcVal)-1)
                else:
                    if self.adcMax != adcVal:
                        rt = self.rs / ((self.adcMax/adcVal)-1)
                    else:
                        rt = self.rs

                a = 1.0/T0_25C + 1.0/self.beta * log(rt/r0) 
                T = 1.0/a
                T = T + self.offset
                if self.get_config_value("TEMP_UNIT", "C") == "C":
                    T = T - 273.15
                if T < 0.0:
                    T = 0.0
            else:
                T = 0.0

            self.value = round(T, 2)

            self.push_update(self.value)
            await asyncio.sleep(self.delay)

    def get_state(self):
        return dict(value=self.value)

def setup(cbpi):
    cbpi.plugin.register("NTCSensor", NTCSensor)
    try:
        # Global Init
        call(["modprobe", "i2c_dev"])
    except Exception as e:
        pass
