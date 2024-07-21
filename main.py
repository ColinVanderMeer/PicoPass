# PicoPass main
# AI was used to help debug a few async errors (Claude 3.5 Sonnet)
import network
import socket
import time
from picozero import pico_temp_sensor, pico_led
import machine
import asyncio
import urequests

networkList = []

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
    networkList.clear()
    networks = wlan.scan()
    for tup in networks:
        ssidName = tup[0].decode("utf-8")
        if ssidName != "":
            networkList.append(ssidName)
            
async def search_picopass(items_list):
    return [item for item in items_list if "PicoPass" in item]

async def getData(ssid):
    attempts = 0
    #Connect to WLAN
    wlan.connect(ssid, "PicoPassword")
    while not wlan.isconnected():
        print('Waiting for connection...')
        await asyncio.sleep(1)
        attempts += 1
        if attempts == 10:
            return "ERROR: Connection timeout"

    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')

    try:
        # Use socket for async operation
        _, _, host, path = "http://192.168.4.1/".split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        
        response = ''
        while True:
            data = s.recv(100)
            if data:
                response += str(data, 'utf8')
            else:
                break
        s.close()
        
        print("Response received")
        print(response)
    except Exception as e:
        print(f"Error during request: {e}")
        response = f"ERROR: {str(e)}"
    finally:
        wlan.disconnect()
    
    return response

async def main():
    startAP_task = asyncio.create_task(startAP())
    
    while True:
        await scanNetwork()
        print(networkList)
        picoPassList = await search_picopass(networkList)
        
        if picoPassList:
            print("PicoPass Found")
            pico_led.on()
            print(await getData(picoPassList[0]))
        await asyncio.sleep(10)  # Sleep for 5 seconds before scanning again

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ap = network.WLAN(network.AP_IF)
ap.config(essid="PicoPass123", password="PicoPassword")
ap.active(True)
wlan.disconnect()

asyncio.run(main())