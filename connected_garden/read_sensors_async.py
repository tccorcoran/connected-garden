import click
import sys
import json
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from asyncio import sleep
from micropython import const



async def read_sensor():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P0)
    await sleep(1)
    value = chan.value
    return value

async def read_sensors():
    results = {}
    i2c = busio.I2C(board.SCL, board.SDA)
    ads0 = ADS.ADS1115(i2c, address=const(0x48))
    ads1 = ADS.ADS1115(i2c, address=const(0x49))
    soil_sensors = [AnalogIn(ads0, i) for i in range(4)]
    soil_sensors.append(AnalogIn(ads1, 0))
    for i, sensor in enumerate(soil_sensors):
        results[f'soil_sensor_{i}'] = sensor.value
    return results
