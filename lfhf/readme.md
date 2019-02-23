# LF/HFまとめ   
心拍変動(HRV)解析のひとつ   

LF/HF: 交感神経活動の指標 or 自律神経バランス   
＝＞　ストレス指標(0～3: 良好, 2 or 3　～ 5: 注意, 5～: 要注意)   


まずは下のサイトを読む。特に概論   
[ストレスと自律神経の科学](http://hclab.sakura.ne.jp/index.html)   

## Pythonによる実装   
＊基本的に250Hz以上かつ２分以上のデータから求める。データをとる場合はM5Stackでpulse_raw_save.inoを利用。   
   
上のサイトの[RRI時系列の用意](http://hclab.sakura.ne.jp/stress_nervous_rri_interp.html)のページをもとにPythonで実装する。   
lfhf.pyを参照。サンプルデータとして２種類のcsvデータを用意した。
