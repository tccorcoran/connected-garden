from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from asyncio import sleep
from random import randint
from pathlib import  Path
import json
# from connected_garden.read_sensors_async import read_sensor
from connected_garden.read_sensors_async import read_sensors
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

html = Path("templates/index.html").read_text()

async def get_sensor_values():
    await sleep(1)
    return {"sensor0":randint(6000,30000),
            "sensor1":randint(6000,30000),
            "sensor2": randint(6000,30000),
            "sensor3": randint(6000,30000),
            "sensor4": randint(6000,30000)}


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json(await read_sensors())
