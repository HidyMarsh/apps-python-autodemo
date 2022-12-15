# apps-python-autodemo
## 概要：講義でチームデモを自動で行うためのプログラム

### 仕様：
WEBベースの緊急着陸地点を登録＆デモアプリとなっている。
尚、デモを開始するためのdrone-kit python コードを含んでおり、Mission Planner＆SITL＆デモアプリが動作する。
アプリアクセスはブラウザで行う。

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
講義資料の通り
git clone git@github.com:dronekit/dronekit-python.git

### 実行方法：
任意のフォルダーでcloneしたあとにフォルダーへ移動。下記を実行する。
>  python appserv.py

### 関連ファィル
locate.xml  緊急着陸地点の緯度・経度を保存するXMLファィル

### 実行方法：
この後にブラウザーアクセスで緊急着陸地点とデモの自動実行が行える。
アプリアクセスはhttp://localhost:8080/emgl/registで行う。

