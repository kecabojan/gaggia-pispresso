from random import randint

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pid
from temperature_sensor import simulator

app = FastAPI()

app.debug = True

templates = Jinja2Templates(directory=".")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/temperature")
async def get_measured_temperature():
    temp = simulator.get(10) + randint(-20, 20)
    return {'temperature': temp}


@app.post("/temperature/{value}")
async def set_target_temperature(value: int):
    return {'target_temperature': value}


P = 15
I = 0.01
D = 1.1


pid = pid.PID(P, I, D)
pid.SetPoint = 105



temperature = 0
targetPwm = 0
take = 1
# while 1:
#     # readConfig()
#     # read temperature data
#     temperature = simulator.get(targetPwm)
#     #temperature = temp_reader.get()
#     print(f'Tempearture: {temperature}')
#     pid.update(temperature)
#     targetPwm = pid.output
#     targetPwm = max(min(int(targetPwm), 100), 0)
#
#     print(f'Take: {take} | Target: {targetT:.1f} C | Current: {temperature:.1f} C | PWM: {targetPwm} %')
#
#     if temperature >= targetT:
#         simulator.set(targetT - 1)
#
#     take += 1
#     time.sleep(0.5)
