import click
from statistics import stdev, mean
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

 
@click.command()
@click.option("--data-points", "-d", type=int, default=20)
def calibrate(data_points):
    values = []
    while len(values) < data_points:
        values.append(chan.value)
    click.secho(f"std : {stdev(values)}:.2f")
    click.secho(f"mean: {mean(values)}:.2f")
    click.secho(f"min: {min(values)}:.2f")
    click.secho(f"max: {min(values)}:.2f")
