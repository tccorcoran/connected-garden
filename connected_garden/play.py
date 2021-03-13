import click
import sys
import json
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from micropython import const

def read_json(json_path):
    with open(json_path) as fi:
        data = json.load(fi)
    context_mean_pairs = sorted([(context, d['mean']) for context, d in data.items() ], key=lambda x: x[1])

    return context_mean_pairs
def print_value(chan, context_mean_pairs):
    value = chan.value
    for i, (context, mean) in enumerate(context_mean_pairs):
        if i == 0 and value <= mean:
            return context
            break
        if value > mean:
            if i == len(context_mean_pairs) -1:
                return context
                break
            if value >= context_mean_pairs[i+1][1]:
                continue
            if value <= (context_mean_pairs[i+1][1] - mean)/2 + mean:
                return context
                break
            else:
                context = context_mean_pairs[i + 1][0]
                return context
                break

@click.command()
@click.option("--input", '-i', type=str, required=True)
def play(input):
    context_mean_pairs = read_json(input)
    i2c = busio.I2C(board.SCL, board.SDA)
    ads0 = ADS.ADS1115(i2c, address=const(0x48))
    ads1 = ADS.ADS1115(i2c, address=const(0x49))
    while True:
        chans= [AnalogIn(ads0, i) for i in range(4)]
        chans.append(AnalogIn(ads1, 0))
        contexts = []
        for i,chan in enumerate(chans):
            context = print_value(chan, context_mean_pairs)
            contexts.append(context)
        print(contexts)
        time.sleep(1)
if __name__ == "__main__":
    play()
