"""
wifiAPから緯度経度を取得(Linux)
"""

import subprocess
import requests
import json

url= "https://location.services.mozilla.com/v1/geolocate?key=test"

iwlist = subprocess.Popen(["sudo", "iwlist", "wlan0", "scan"], stdout=subprocess.PIPE)
grep = subprocess.Popen(["grep", "-e", "Address:", "-e", "Signal"],
            stdin=iwlist.stdout, stdout=subprocess.PIPE)
grep = grep.communicate()[0].splitlines()

wifiAccessPoints = []

for add, level in zip(grep[::2], grep[1::2]):
    mac_address = add.split()[4].decode('utf-8')
    signal_level = int(level.split()[2][6:])
    wifiAccessPoints.append({"macAddress":mac_address, "signalStrength":signal_level})

print(wifiAccessPoints)

json_data = json.dumps({"wifiAccessPoints":wifiAccessPoints}).encode("utf-8") #文字列に変換

response = requests.post(url, data=json_data, headers={'Content-type':'application/json'})

content = response.json()

lat = content['location']['lat']    #緯度
lng = content['location']['lng']    #経度
radius = content['accuracy']        #正確さ（半径）

print(lat, lng, radius)
