from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from asyncio import sleep
from random import randint
from pathlib import  Path
import io
import json
import base64
from connected_garden.read_sensors_async import read_sensors
from connected_garden.plot import df_to_html
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

html = Path("templates/index.html").read_text()

vid_template = Path("templates/video.html").read_text()
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
try:
    import picamera
    camera = picamera.PiCamera()
    camera.start_preview()
    camera.resolution = (640,480)
except ImportError:
    logger.warn("Picamera is not installed!")

async def get_sensor_values():
    await sleep(1)
    return {"soil_sensor_0":randint(6000,30000),
            "soil_sensor_1":randint(6000,30000),
            "soil_sensor_2": randint(6000,30000),
            "soil_sensor_3": randint(6000,30000),
            "soil_sensor_4": randint(6000,30000),
            "light_sensor": randint(0,100000),
            "air_humidity": randint(0,100),
            "air_temp": randint(0,100)}


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/plot")
async def get():
    graph = df_to_html("static/test_csv.csv")
    return HTMLResponse(graph)

@app.get("/sensors")
async def get_sensors():
    return await read_sensors(time_sleep=0)

@app.get("/stream")
async def get():
    return HTMLResponse(vid_template)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        sio = io.BytesIO()
        camera.capture(sio, "jpeg", use_video_port=True)
        resp = await read_sensors()
        resp['image_data'] = base64.b64encode(sio.getvalue()).decode('utf8')
        await websocket.send_json(resp)

@app.websocket("/video-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        sio = io.BytesIO()
        camera.capture(sio, "jpeg", use_video_port=True)
        await websocket.send_text(base64.b64encode(sio.getvalue()).decode('utf8'))
