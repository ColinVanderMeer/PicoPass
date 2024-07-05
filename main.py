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
