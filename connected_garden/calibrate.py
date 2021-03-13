import click
import sys
import json
from statistics import stdev, mean, median
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from micropython import const


def collect_data(num_data_points, sensor_no):
    i2c = busio.I2C(board.SCL, board.SDA)
    ads0 = ADS.ADS1115(i2c, address=const(0x48))
    ads1 = ADS.ADS1115(i2c, address=const(0x49))
    chans = [AnalogIn(ads0, i) for i in range(4)]
    chans.append(AnalogIn(ads1, 0))
    chan = chans[sensor_no]
    values = []
    chan.value;time.sleep(.5) # discard the first data point
    while len(values) < num_data_points:
        values.append(chan.value)
        click.secho(str(chan.value))
        time.sleep(.5)
    results = {}
    results['mean'] = mean(values)
    results['std']  = stdev(values)
    results['min'] = min(values)
    results['max'] =max(values)
    results['median'] = median(values)
    click.secho(f"std : {results['std']:.2f}")
    click.secho(f"mean: {results['mean']:.2f}")
    click.secho(f"min : {min(values):.2f}")
    click.secho(f"max : {max(values):.2f}")
    return results

@click.command()
@click.option("--num-data-points","-n", type=int, default=20)
@click.option("--output", '-o', type=str, default="calibrated.json")
def calibrate(num_data_points, output):
    results = {str(i):{} for i in range(5)}
    while True:
        if click.confirm("Finish collecting all data?"):
            with open(output, 'w') as fo:
                json.dump(results,fo, indent=2)
            click.secho(f"Wrote results to {output}", fg='green')
            sys.exit(0)
        context = click.prompt("sensor context", type=str)
        while True:
            sensor_no = click.prompt("Sensor number", type=int)
            context_data = collect_data(num_data_points, sensor_no)
            click.secho(f"Done collecting data for {context}", fg='green')
            results[str(sensor_no)][context] = context_data
            if click.confirm('Add another sensor?'):
                continue
            else:
                click.secho(f"Done collecting data for {sensor_no} ")
                break

if __name__ == "__main__":
    calibrate()