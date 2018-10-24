# pythonでwebAPI(サーバー側)

## 1, APIサーバーとは   
[pythonでwebAPI](https://github.com/tanopanta/benkyooo/tree/master/api_benkyo)ではAPIを利用する（クライアント）側の機能を利用した。
今回はAPIを発行する側(WEBサーバー)を学ぶ。API周りはIoTをする上で基本となるのでぜひ理解しておいてほしい。   

＊APIではHTTPのGETメソッドとPOSTメソッドの2種類を利用するが、この違いが分からない場合は先に調べておいてください。簡単にいうとGETはデータをもらうだけの場合、POSTはデータを送りつつ結果をもらう場合に使う(場合が多い)。前回の例でいうと天気をもらうのはGETで、WiFiのテータを送って位置情報をもらうのはPOST。   
＊データの可視化に関してはambientというサービスが無料で利用できるらしいので、誰か試してみてくれたらうれしいな。ラズパイやESP32から利用するサンプルもありますよ。   

## 2, 基本形   
Pythonで簡単に使えるウェブアプリケーションフレームワークとしてはFlaskが有名なのでこれを利用する。まずはFlaskを```conda install flask```等によりインストールする。   

インストールが終わったら以下のサンプルを試してみる。これを実行するとFlask内蔵のWEBサーバーが立ち上がり、GETメソッドによりアクセスできる。例えば(http://127.0.0.1:5000) にアクセスすれば文字が表示される。   

一般にウェブフレームワークにはルーティングという機能があり(@app.route()に対応)、これによりURLと処理との対応付けが簡単にできる。Flaskの場合、returnで何かの文字列を返すことで動作する。
```Python
#APIサーバー基本形
from flask import Flask, request
app = Flask(__name__)

#インデックス(例　http://127.0.0.1/)にアクセスしたときの処理
@app.route("/") #@から始まる行はデコレーター(修飾子)であり直下の関数に機能を追加する。
def hello():
    return "hello world!!"

#/testにアクセスしたときの処理
@app.route("/test")
def test():
    return "test"

if __name__ == "__main__":
    app.debug = True #デバッグモードをオン
    app.run(host='0.0.0.0') #host='0.0.0.0'で外からのアクセスを受けつける
```
プログラムからアクセスする場合
```Python
import requests

url = "http://127.0.0.1:5000"

response = requests.get(url) #GETでAPIを叩く

print(response.text)

```
[[Python] Flask 入門](http://python.zombie-hunting-club.com/entry/2017/11/03/223503)にはHTMLを表示する方法が載っているので興味があればぜひ

## 3, POSTメソッドを利用する。  
２ではHTTPのGETメソッドを利用したが、センサーデータの送信等にはPOSTメソッドとJSONの組み合わせを使う場合が多い。POSTメソッドを利用するのは以下のようになる。   
ポイントとしては **@app.route()** の引数で **methods=['POST']** と指定しメソッドをPOSTに限定する点と、**request.json**で受け取ったJSONを取得する点。
```Python
#POST(サーバー)
#post server

from flask import Flask, request, Response
import json

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    return "aaaa"

# /post にアクセスしたときの処理
@app.route('/post', methods=['POST'])
def post():
    js_dict = request.json 
    print(js_dict)

    return Response(json.dumps({"result":"OK"}))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に

```
プログラムからアクセスする。JSONを文字列として送信。
```Python
#POST(クライアント)
import requests
import json

url = "http://127.0.0.1:5000/post"

data = {"name":"あいう えお"}
json_str = json.dumps(data) #文字列に変換
response = requests.post(url, data=json_str, headers={'Content-type':'application/json'}) 

print(response.text)
```
## 4, 実例   
実例として、ラズパイで10秒ごとにセンサーデータを得てそれをPOSTメソッドによりサーバで保存するものを作る。   
センサーは、各自好きなものを使えばよい。サンプルとしてはラズパイのCPUの温度を取得している。
```Python
#(クライアント)
from datetime import datetime
import time
import requests
import json

url = "http://[サーバー側のアドレス]:5000/post"

for i in range(10):
    #センサーデータを取得-------
    from subprocess import getoutput

    temp = getoutput("vcgencmd measure_temp").split('=') #CPU温度を取得
    print(temp)
    sensor = temp[1]

    #----------------------
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S") #現在時刻を取得

    data = {"date": now, "data": sensor}
    json_str = json.dumps(data) #文字列に変換
    response = requests.post(url, data=json_str, headers={'Content-type':'application/json'}) 

    print(response.text)
    time.sleep(10.0) #10秒待機

```
サーバー側。さっきのサンプルの一部を変更
```Python
#サーバー側

from flask import Flask, request, Response
import json

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    return "aaaa"

# /post にアクセスしたときの処理
@app.route('/post', methods=['POST'])
def post():
    js_dict = request.json 
    #サンプルとの変更点-----
    print(js_dict["date"], js_dict["data"])
    with open("out.csv", "a") as f:
        f.write("{0}, {1}\n".format(js_dict["date"], js_dict["data"]))
    #----------------------------
    return Response(json.dumps({"result":"OK"}))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に

```
## 5, 利用例   
例えば次のような利用例が考えられる   
- ラズパイにサーバーを立てるパターン
    - GETメソッドでアクセスしたらセンサーデータを返す
    - ブラウザ上でラズパイの電源を切る、GPIOをONにする等の操作
- PCにサーバーを立てるパターン
    - ラズパイ(M5Stack)に保存されたCSVデータをPOSTでアップロード
    - HTMLを組み合わせてデータの可視化

and more...