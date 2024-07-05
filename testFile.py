import network
import socket
import time
from picozero import pico_temp_sensor, pico_led
import machine

import asyncio

async def scanNetwork():
    print("21")
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    print("22")
    wlan.active(True)
    print("23")
    networks = wlan.scan()
    print("24")
    print(networks)
    print("25")
    
async def web_page():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
              <body><h1>Hello World</h1></body></html>
           """
    return html

async def ap_mode(ssid, password):
    """
        Description: This is a function to activate AP mode
        
        Parameters:
        
        ssid[str]: The name of your internet connection
        password[str]: Password for your internet connection
        
        Returns: Nada
    """
    # Just making our internet connection
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    while not ap.active():
        await asyncio.sleep(1)  # Sleep asynchronously

    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating socket object
    s.bind(('', 80))
    s.listen(5)
    s.setblocking(False)  # Set socket to non-blocking mode

    loop = asyncio.get_event_loop()

    while True:
        try:
            conn, addr = await loop(s.accept())
            print('Got a connection from %s' % str(addr))
            request = await loop.sock_recv(conn, 1024)
            print('Content = %s' % str(request))
            response = await web_page()
            await loop.sock_sendall(conn, response.encode())  # Ensure the response is in bytes
            conn.close()
        except OSError as e:
            if e.errno != 11:  # EAGAIN
                raise
            await asyncio.sleep(1)

async def main():
    ap_task = asyncio.create_task(ap_mode('NAME', 'PASSWORD'))
    await asyncio.sleep_ms(5_000)
    scan_task = asyncio.create_task(scanNetwork())

    await asyncio.sleep_ms(10_000)

asyncio.run(main())
