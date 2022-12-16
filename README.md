# apps-python-autodemo
## 概要：講義でチームデモを自動で行うためのプログラム

### 仕様：
WEBベースの緊急着陸地点を登録＆デモアプリとなっている。
尚、デモを開始するためのdrone-kit python コードを含んでおり、Mission Planner＆SITL＆デモアプリが動作する。
アプリアクセスはブラウザで行う。

![App WEB TOP](https://github.com/HidyMarsh/apps-python-autodemo/blob/master/img/appserv.png)

### インストールに関して：
現実的にFlight Controllerにこのアプリを入れて使うことは無いが導入するとしたらコンパニオンコンピュターと考えています。
今回は修了のデモということで環境が限られているのでSITLと同じ環境Ubuntuへ導入
アプリケーションはpythonのみで作成した。

### 将来的には：
いずれdronekit-androidで同じ事を実現したい。 

### インストール環境構築：
# bottle framework
下記を実行
> pip  install  bottle
# dronekit-python
講義資料の通り<br>
(git clone git@github.com:dronekit/dronekit-python.gita)

### プログラム実行方法：
任意のフォルダーでcloneしたあとにフォルダーへ移動。下記を実行する。
>  python appserv.py

### 関連ファィル
locate.xml  緊急着陸地点の緯度・経度を保存するXMLファィル

### アプリ操作方法：
この後にブラウザーアクセスで緊急着陸地点とデモの自動実行が行える。
アプリアクセスは (http://localhost:8080/emgl/regist) で行う。

緊急着陸地点は経度、緯度共にint整数値で入力すること、通常は浮動小数点の値だが
浮動小数点を外して入力するだけでOK

DMEOボタンは下部に２つ用意しているがFailSafeが働くタイミングをAutoモード移行後
２０秒と５０秒で用意している。

ただし任意の値にしたいなら下記のURLでアクセスしてもOKです。
(http://localhost:8080/emgl/do_emgl/整数値)<br>
例：(http://localhost:8080/emgl/do_emgl/40)

### このアプリを使う構成の想定手順とデモ手順
最初にMPを起動、SITLを起動します。一番最後に本アプリをプログラム実行します。
次にフライプランをMPで作成もしくは読み込みをします。書き込み済んだらデモの準備はOKです。
WEBブラウザーで (http://localhost:8080/emgl/regist) へ接続し下部のデモボタンを押して開始
してください。
予め登録した着地点を計算しバッテリーフェイルが発生した際に一番近距離の場所へ移動し着地を行います。
