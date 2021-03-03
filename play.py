import click
import sys
import json
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def read_json(json_path):
    with open(json_path) as fi:
        data = json.load(fi)
    context_mean_pairs = sorted([(context, d['mean']) for context, d in data.items() ], key=lambda x: x[1])

    return context_mean_pairs

@click.command()
@click.option("--input", '-i', type=str, required=True)
def play(input):
    context_mean_pairs = read_json(input)
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    while True:
        chan = AnalogIn(ads, ADS.P0)
        value = chan.value
        for i, (context, mean) in enumerate(context_mean_pairs):
            if i == 0 and value <= mean:
                click.secho(f"{value}: {context}")
                break
            if value > mean:
                if i == len(context_mean_pairs) -1:
                    click.secho(f"{value}: {context}")
                    break
                if value >= context_mean_pairs[i+1][1]:
                    continue
                if value <= (context_mean_pairs[i+1][1] - mean)/2 + mean:
                    click.secho(f"{value}: {context}")
                    break
                else:
                    context = context_mean_pairs[i + 1][0]
                    click.secho(f"{value}: {context}")
                    break
        time.sleep(.5)
if __name__ == "__main__":
    play()