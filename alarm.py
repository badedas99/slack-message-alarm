import requests
import websockets
import asyncio
import json
import RPi.GPIO as GPIO
import time
import configparser

config = configparser.ConfigParser()

config.read('config.ini')

URL = "https://slack.com/api/rtm.connect"
PARAMS = {'token': config['DEFAULT']['token']}

response = requests.get(url=URL, params=PARAMS)

url = response.json()['url']

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)


async def webhook():
    async with websockets.connect(url) as websocket:
        while True:
            msg = await websocket.recv()
            msg = json.loads(msg)
            if 'channel' in msg and \
                'type' in msg and \
                    msg['channel'] == config['DEFAULT']['channel'] and \
                    msg['type'] == 'message' and \
                    msg['text'].lower() != 'thought of the week':
                GPIO.output(23, GPIO.LOW)
                print(msg['text'])
                time.sleep(int(config['DEFAULT']['time']))
                GPIO.output(23, GPIO.HIGH)

asyncio.get_event_loop().run_until_complete(webhook())
