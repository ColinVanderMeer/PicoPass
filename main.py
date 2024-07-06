import network
import socket
import time
from picozero import pico_temp_sensor, pico_led
import machine
import asyncio

async def handle_client(conn, addr):
    print('Got a connection from %s' % str(addr))
    conn.setblocking(False)
    request = b""
    try:
        while True:
            try:
                chunk = conn.recv(1024)
                if chunk:
                    request += chunk
                    if b"\r\n\r\n" in request:
                        break
                else:
                    # No data received, connection might be closed
                    break
            except OSError as e:
                if e.args[0] != 11:  # EAGAIN
                    raise
                await asyncio.sleep(0.1)
        
        if request:
            print('Content = %s' % str(request))
            response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nTestResponse"
            conn.send(response.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

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
            asyncio.create_task(handle_client(conn, addr))
        except OSError as e:
            if e.args[0] != 11:  # 11 is EAGAIN, meaning no data available
                print("Unexpected error:", e)
        await asyncio.sleep(0.1)

async def scanNetwork():
    networks = wlan.scan()
    print(networks)
    for listItem in networks:
        print(listItem)

async def main():
    startAP_task = asyncio.create_task(startAP())
    
    while True:
        await scanNetwork()
        await asyncio.sleep(10)  # Sleep for 5 seconds before scanning again

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ap = network.WLAN(network.AP_IF)
ap.config(essid="PicoPass678", password="PicoPassword")
ap.active(True)
wlan.disconnect()

asyncio.run(main())