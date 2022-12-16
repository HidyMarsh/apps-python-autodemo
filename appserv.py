from bottle import request,route, run, template, static_file
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from dronekit import connect, VehicleMode, Command
import os,sys,time

#静的コンテンツのリクエスト処理
@route('/emgl/<filename>',method='GET')
def static_read(filename):
    return static_file(filename,root='./static/')

#自動航行デモを実行するメソッド
#causetime引数はAutoモード発生からバッテリーFailsafeを効かせるまでの間隔の指定
@route('/emgl/do_emgl/<causetime>',method='GET')
def emgl_call(causetime):
    #接続処理
    vehicle = connect('tcp:127.0.0.1:5763',wait_ready=True, timeout=30)
    #バッテリー電圧を平常にセット
    vehicle.parameters['SIM_BATT_VOLTAGE']= 11.1

    try:
       #アーム可能状態まで待つ
       vehicle.wait_for_armable()
       #GUIDEDモードへ移行
       vehicle.wait_for_mode("GUIDED")
       #飛行可能にする
       vehicle.arm()
       #遅延入れてtakeoffに入れるようにタイミングを取る。
       time.sleep(1)
       #離陸処理に入る。
       vehicle.wait_simple_takeoff(10, timeout=20)

    except TimeoutError as takeoffError:
       #エラーメッセージ
       print("Takeoff is timeout!!!")
       sys.exit()
    #自動飛行開始のメッセージ
    print("Starting mission")

    #Autoモードに入れて自動飛行モードへ移行
    vehicle.mode = VehicleMode("AUTO")
    #指定時間causetimeに合わせてバッテリー電圧値を下げる設定が発生
    time.sleep(int(causetime))
    #電圧を異常値に設定
    vehicle.parameters['SIM_BATT_VOLTAGE']= 9.7
    #電圧異常が発生したらWEB画面にメッセージを出す。
    return "Now Battery Fail State" 

#TOP画面で経度緯度を緊急着陸地点として登録する。
#デモを開始するボタンを装備
@route('/emgl/regist',method='GET')
def regist_form():
    #localte.xmlは実行環境のフライトコードのパスに設定変更してください。
    tree = ET.parse('locate.xml')
    root = tree.getroot()
    record_line = ""
    for child in root.iterfind("pos"):
        record_line += child.text + '\n'

    #現在の緊急地点登録済みデータをマージして登録画面へ展開
    return template('add_emgl', landing_points = record_line)


#新規で緊急着陸地点を登録する機能。locate.xmlに追記する。
@route('/emgl/write_point/', method='GET')
def regist_emgl():
    #print(request.query.LAT)
    #print(request.query.LNG)
    pos_line = request.query.LAT + '|' + request.query.LNG
    #localte.xmlは実行環境のフライトコードのパスに設定変更してください。
    tree = ET.parse('locate.xml')
    root = tree.getroot()

    add_line = "<pos>" + pos_line + "</pos>\n"
    record_line = ""
    header = '<?xml version="1.0" encoding="utf-8"?>\n<location>\n'
    bottom = "</location>\n"
    for child in root.iterfind("pos"):
        #print(child.text.split('|')[0])
        #print(child.text.split('|')[1])
        record_line += "<pos>" + child.text + "</pos>" + '\n'

    record_line = header + record_line + add_line + bottom
    #print(record_line)

    #localte.xmlは実行環境のフライトコードのパスに設定変更してください。
    f = open('locate.xml', 'w')
    f.write(record_line)
    f.close()
    message = "Successful addition of emergency langing location.<br>"
    back_regurl = "<p><a href='/emgl/regist'>Click to Back Registration Form</a></p>"
    return message + "latitude={lat} longitude={lng}".format(lat=request.query.LAT,lng=request.query.LNG) + back_regurl

# メインメソッドにてWEBサーバデーモンを発生させる。
if __name__ == "__main__":
    run(host="0.0.0.0",port='8080',reloader=True)

