from bottle import request,route, run, template, static_file
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from dronekit import connect, VehicleMode, Command
import os,sys,time


@route('/emgl/<filename>',method='GET')
def static_read(filename):
    return static_file(filename,root='./static/')

@route('/emgl/do_emgl/<causetime>',method='GET')
def emgl_call(causetime):
    vehicle = connect('tcp:127.0.0.1:5763',wait_ready=True, timeout=30)
    vehicle.parameters['SIM_BATT_VOLTAGE']= 11.1

    try:
       vehicle.wait_for_armable()
       vehicle.wait_for_mode("GUIDED")
       vehicle.arm()
       time.sleep(1)
       vehicle.wait_simple_takeoff(10, timeout=20)

    except TimeoutError as takeoffError:
       print("Takeoff is timeout!!!")
       sys.exit()

    print("Starting mission")

    # Set mode to AUTO to start mission
    vehicle.mode = VehicleMode("AUTO")

    time.sleep(int(causetime))
    vehicle.parameters['SIM_BATT_VOLTAGE']= 9.7
    return "Now Battery Fail State" 


@route('/emgl/regist',method='GET')
def regist_form():

    tree = ET.parse('/home/ardupilot/serv/locate.xml')
    root = tree.getroot()
    record_line = ""
    for child in root.iterfind("pos"):
        record_line += child.text + '\n'

    return template('add_emgl', landing_points = record_line)

@route('/emgl/write_point/', method='GET')
def regist_emgl():
    #print(request.query.LAT)
    #print(request.query.LNG)
    pos_line = request.query.LAT + '|' + request.query.LNG
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

    f = open('locate.xml', 'w')
    f.write(record_line)
    f.close()
    message = "Successful addition of emergency langing location.<br>"
    back_regurl = "<p><a href='/emgl/regist'>Click to Back Registration Form</a></p>"
    return message + "latitude={lat} longitude={lng}".format(lat=request.query.LAT,lng=request.query.LNG) + back_regurl


if __name__ == "__main__":
    run(host="0.0.0.0",port='8080',reloader=True)

