# pythonでwebAPI

## 1, apiとは
決まった形式で尋ねたら返事をしてくれる仕組み
- urlのパラーメーター XML JSON

## 2, JSONとは
JSON(JavaScript Object Notation)
```
{
    "name": "ogawa",
    "object" {
        "a": 2,
        "b": 3.3
    }
}
```

## 3, 天気を取得 tenki.py
[pythonを使ってOpenWeatherMapから天気情報を取得](https://qiita.com/iton/items/87d4846de15736b599e4)
## 4, 緯度経度から天気を取得 tenkibygeo.py
[API詳細](https://openweathermap.org/current)
## 5, wifiAPから緯度経度取得 geo.py
Mozillaのページ   
[Mozilla Location Service APIs](https://mozilla.github.io/ichnaea/api/geolocate.html)   
[Algorithms](https://mozilla.github.io/ichnaea/algo/index.html)   
概念   
[Wi-Fi positioning system - Wikipedia(en)](https://en.wikipedia.org/wiki/Wi-Fi_positioning_system)   


## 6, wifiAPから天気 
4と5を合わせればできるはず   


次回　apiサーバー(WEBサービス))の作り方 か　LF/HFの計算
