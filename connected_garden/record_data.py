import pandas as pd
import click
import requests
import logging
import os
from datetime import datetime
import time
from collections import defaultdict
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_data(host="192.168.1.5", retry_n=0):
    try:
        resp = requests.get(f"http://{host}:8000/sensors")
    except Exception as e:
        logger.error(e)
        if retry_n < 3:
            return get_data(host=host,retry_n=retry_n+1)
        return {}
    return resp.json()

@click.command("collect-data")
@click.option("--csv_path", '-o', required=True)
@click.option("--host", "-h", default="192.168.1.5")
@click.option("--max_temp_records", "-r", default=30,type=int)
@click.option("--time_sleep", '-t', default=30, type=int)
def collect_and_write(csv_path, host, max_temp_records, time_sleep):

    tmp_data = defaultdict(list)
    df = pd.DataFrame()
    while True:
        try:
            time.sleep(time_sleep)
            sensor_data = get_data(host=host)
            for key, value in sensor_data.items():
                tmp_data[key].append(value)
            tmp_data['timestamp'].append(datetime.now())
            logger.debug(f"Collected 1 record: {sensor_data}")
            if len(tmp_data['timestamp']) >= max_temp_records:
                logger.info(f"writing dataframe to {csv_path}")
                headers=True
                if os.path.exists(csv_path):
                    headers = False
                df = pd.DataFrame(tmp_data)
                df.set_index("timestamp")
                df.to_csv(csv_path,mode='a', header=headers, index=False)
                tmp_data = defaultdict(list)
        except Exception as e:
            logger.error(e)
            df.to_csv(csv_path,mode='a')

if __name__ == "__main__":
    collect_and_write()