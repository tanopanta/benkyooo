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
