import network
import socket
import time
from picozero import pico_temp_sensor, pico_led
import machine

import asyncio
    
async def startAP(ssid, password):
    print("start")
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    while not ap.active():
        await asyncio.sleep(1)  # Sleep asynchronously

    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])

async def scanNetwork():
    # Connect to WLAN
    networks = wlan.scan()
    print(networks)

async def main():

    startAP_task = asyncio.create_task(startAP("test123", "toor"))

    while True:
        scanForPico_task = asyncio.create_task(scanNetwork())
        await asyncio.sleep_ms(5_000)
        
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

asyncio.run(main())
