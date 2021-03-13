from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from asyncio import sleep
from random import randint
from pathlib import  Path
import json
#from connected_garden.read_sensors_async import read_sensors
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

html = Path("templates/index.html").read_text()

async def get_sensor_values():
    await sleep(1)
    return {"soil_sensor_0":randint(6000,30000),
            "soil_sensor_1":randint(6000,30000),
            "soil_sensor_2": randint(6000,30000),
            "soil_sensor_3": randint(6000,30000),
            "soil_sensor_4": randint(6000,30000),
            "air_temp": randint(0,100)}


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json(await get_sensor_values())
