# 感情と心拍の関係を調べる   
心拍間隔の計測と保存、感情の取り方を知る。(全部スマホで操作する想定)   

## ラズパイ起動＋SSH接続
事前にSSHクライアントアプリとFingというアプリを入れる。
1. ラズパイの電源を入れて、ラズパイと同じwifi内にスマホも接続。
1. Fingでwifi内をスキャン。RaspberryPiと書いてあるところのIPアドレスを見る。（ここでお気に入りに登録しておくと便利）
1. SSHクライアントアプリに移動して、先ほどのIPアドレスでログイン。
##  感情の記録用WEBアプリを開く
感情の記録用WEBアプリにブラウザで接続する。(アドレスはSlack参照)心拍の計測をする前にとりあえず一個分ぐらい感情データを入れておく。   
＊これのソースコードはプライベートリポジトリにあるので、もし見たかったらGithubのアカウントを作ってアカウント名を教えてください。
## 計測をする
心拍の情報をとりつつ感情も報告する
。sshクライアントで以下のように心拍を計測。  
1. `cd keisoku`
1. `python3 rri_save.py ＊＊jk＊＊＊ -t 計測時間(秒)`   

心拍データは `data/＊＊jk＊＊＊/` に保存される。  
心拍情報は2Hzの心拍間隔データ(RRI)として保存されるので、心拍数として見たい場合はそれぞれを60から割ればよい。

## 心拍と感情との対応を調べるときは
サーバー機のPCで、DB Browser for SQLiteを起動し、左上のfile->下の方のlabel.dbを開き、感情のデータを確認する。(file->export->Tables as csv file　でcsvとして保存もできる)  
これと先ほどの心拍間隔データをIDやタイムスタンプをもとに比較し、相関を見る。