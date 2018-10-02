"""
APIで天気を取得
"""
import requests
import json

city_name = "Matsudo" # 主要な都市名はいけるっぽい。
API_KEY = "750d9f39ed5313c3f1a8139bba105580"
api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={key}"

url = api.format(city = city_name, key = API_KEY)

print(url)

response = requests.get(url) #GETでAPIを叩く
data = response.json() #もらったJSON文字列をpythonの辞書型へ変換

print(data)

"""
jsonText = json.dumps(data, indent=4)
print(jsonText)
"""