import network
import socket
import time
from picozero import pico_temp_sensor, pico_led
import machine
import asyncio

async def startAP():
    while not ap.active():
        await asyncio.sleep(1)  # Sleep asynchronously
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
    s.setblocking(False)
    
    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            print('Content = %s' % str(request))
            response = "TestResponse"
            conn.send(response)
            conn.close()
        except OSError as e:
            if e.args[0] == 11:  # EAGAIN error, meaning no data available
                pass
            else:
                print("Unexpected error:", e)
        await asyncio.sleep(0.1)

async def scanNetwork():
    print("Scanning network")
    networks = wlan.scan()
    print(networks)
    for listItem in networks:
        print(listItem)

async def main():
    startAP_task = asyncio.create_task(startAP())
    
    print("we got here")
    
    while True:
        print("we here tooo :3")
        print("test")
        await scanNetwork()
        print("here?")
        await asyncio.sleep(10)  # Sleep for 5 seconds before scanning again

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ap = network.WLAN(network.AP_IF)
ap.config(essid="PicoPass678", password="PicoPassword")
ap.active(True)
wlan.disconnect()

asyncio.run(main())