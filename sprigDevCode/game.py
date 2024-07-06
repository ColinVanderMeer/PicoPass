import machine
import time
import network
import socket
import urequests

adcpin = 4
sensor = machine.ADC(adcpin)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

networkList = []

def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

def scanNetwork(spryg):
    # Connect to WLAN
    i = 0
    networks = wlan.scan()
    for tup in networks:
        ssidName = tup[0].decode("utf-8")
        if ssidName != "":
            spryg.screen.text(ssidName, 0, i, 0xFFFF)
            networkList.append(ssidName)
        i += 10
    return i

def search_picopass(items_list):
    return [item for item in items_list if "PicoPass" in item]

def getData(ssid):
    attempts = 0
    #Connect to WLAN
    wlan.connect(ssid, "PicoPassword")
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
        attempts += 1
        if attempts == 10:
            return "ERROR"
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')

    response = urequests.get("http://192.168.4.1")
    
    print(response.text)
    wlan.disconnect()
    
    return response.text


def run(spryg):
    refreshTimes = 0
    while True:
        networkList.clear()
        spryg.screen.fill(0x0000)
        textBuf = scanNetwork(spryg)
        spryg.screen.text(str(refreshTimes), 0, textBuf, 0x00FF)
        
        picoPassList = search_picopass(networkList)
        
        if picoPassList:
            spryg.screen.text("PicoPass Found", 0, textBuf+10, 0xFF00)
            spryg.screen.text(getData(picoPassList[0]), 0, textBuf+20, 0x0FF0)
            
        
        spryg.flip()
        
        refreshTimes += 1
        time.sleep(5)