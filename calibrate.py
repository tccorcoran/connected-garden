import click
import sys
import json
from statistics import stdev, mean
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn



def collect_data(num_data_points):
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P0)
    values = []
    while len(values) < num_data_points:
        values.append(chan.value)
        click.secho(str(chan.value))
        time.sleep(.5)
    results = {}
    results['mean'] = mean(values)
    results['std']  = stdev(values)
    results['min'] = min(values)
    results['max'] =max(values)
    click.secho(f"std : {results['std']:.2f}")
    click.secho(f"mean: {results['mean']:.2f}")
    click.secho(f"min : {min(values):.2f}")
    click.secho(f"max : {max(values):.2f}")
    return results

@click.command()
@click.option("--num-data-points","-n", type=int, default=20)
@click.option("--output", '-o', type=str, default="calibrated.json")
def calibrate(num_data_points, output):
    results = {}
    while True:
        context = click.prompt("sensor context", type=str)
        context_data = collect_data(num_data_points)
        click.secho(f"Done collecting data for {context}", fg='green')
        results[context] = context_data
        if click.confirm('Do you want to continue?'):
            continue
        else:
            with open(output, 'w') as fo:
                json.dump(results,fo, indent=2)
            click.secho(f"Wrote results to {output}", fg='green')
            sys.exit(0)

if __name__ == "__main__":
    calibrate()