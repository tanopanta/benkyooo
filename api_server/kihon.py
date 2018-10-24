#APIサーバー基本形
from flask import Flask, request
app = Flask(__name__)

#インデックス(例　http://127.0.0.1/)にアクセスしたときの処理
@app.route("/")
def hello():
    return "hello world!!"

#/testにアクセスしたときの処理
@app.route("/test")
def test():
    return "test"

if __name__ == "__main__":
    app.debug = True #デバッグモードをオン
    app.run(host='0.0.0.0') #host='0.0.0.0'で外からのアクセスを受けつける