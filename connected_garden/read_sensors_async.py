import click
import sys
import json
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_am2320
import adafruit_bh1750

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
    await sleep(.5)
    i2c = busio.I2C(board.SCL, board.SDA)
    ads0 = ADS.ADS1115(i2c, address=const(0x48))
    ads1 = ADS.ADS1115(i2c, address=const(0x49))
    air_meter = adafruit_am2320.AM2320(i2c)
    light_meter = adafruit_bh1750.BH1750(i2c)

    soil_sensors = [AnalogIn(ads0, i) for i in range(4)]
    soil_sensors.append(AnalogIn(ads1, 0))
    for i, sensor in enumerate(soil_sensors):
        results[f'soil_sensor_{i}'] = sensor.value
    results['air_temp'] = air_meter.temperature*(9/5) + 32
    results['air_humidity']  = air_meter.relative_humidity
    results['light_meter']  = light_meter.lux
    return results

