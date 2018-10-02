"""
APIで天気を取得(緯度経度から)
"""

import requests
import json


lat = 35.747 #緯度
lng = 139.805 #経度

API_KEY = "750d9f39ed5313c3f1a8139bba105580"
api = "http://api.openweathermap.org/data/2.5/weather?units=metric&lat={lat}&lon={lng}&APPID={key}"

url = api.format(lat = lat, lng = lng, key = API_KEY)

print(url)

response = requests.get(url)
data = response.json()

print(data["main"]["temp"])