#!/usr/bin/python
from bottle import route,run,get,post,response,static_file,request
import cv2,cv
from controlServer import *

cam=cv2.VideoCapture(0)
if cam.isOpened()==False:
    print("cant open cam")
    exit()
cam.set(cv.CV_CAP_PROP_FRAME_WIDTH,320)
cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT,240)

@get('/stream')
def do_stream():
    response.set_header('Content-Type', 'multipart/x-mixed-replace; boundary=--MjpgBound')
    while True:
        ret,image = cam.read()
        jpegdata=cv2.imencode(".jpeg",image)[1].tostring()
        string = "--MjpgBound\r\n"
        string += "Content-Type: image/jpeg\r\n"
        string += "Content-length: "+str(len(jpegdata))+"\r\n\r\n"
        string += jpegdata
        string += "\r\n\r\n\r\n"
        yield string

#control rccar
@post('/motor')
def control_rccar():
    command=request.forms.get('command')
    print command
    if command == "GO":
        forward()
    elif command == "LEFT":
        left()
    elif command == "STOP":
        stop()
    elif command == "RIGHT":
        right()
    elif command == "BACK":
        backward()
    return ''


@route('/')
def do_route():
    return static_file("index.html", root=".")

initMotors()
run(host='<IP address>', port=8080, server='paste')
