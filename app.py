"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
import cv2
import numpy as np
import base64

import torch
from flask import Flask, render_template, request, redirect, Response
from flask_socketio import emit, SocketIO

#Temp---------------------------------
import pathlib
temp = pathlib.PosixPath

if os.name == 'nt':
    pathlib.PosixPath=pathlib.WindowsPath
#-------------------------------------

app = Flask(__name__)
sio = SocketIO(app)
sio.init_app(app, cors_allowed_origins="*")

#'''
# Load Pre-trained Model
# model = torch.hub.load(
#         "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
#         )#.autoshape()  # force_reload = recache latest code
#'''
# Load Custom Model
model = torch.hub.load("ultralytics/yolov5", "custom", path = "./bestv2.pt", force_reload=True)

# Set Model Settings
model.eval()

# Jangan Lupa Diganti
model.conf = 0.6  # confidence threshold (0-1)
model.iou = 0.45  # NMS IoU threshold (0-1) 

from io import BytesIO

def gen():
    cap=cv2.VideoCapture(0)
    while(cap.isOpened()):
        success, frame = cap.read()
        if success == True:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
            img = Image.open(io.BytesIO(frame))
            results = model(img, size=640)
            img = np.squeeze(results.render()) #RGB
            # read image as BGR
            img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #BGR
        else:
            break

        frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()
        #print(frame)
        
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
'''                        
@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
'''

from flask import request, jsonify

@sio.on("image")
def procImg(data):
    sbuf = io.StringIO()
    sbuf.write(data)
    img = Image.open(io.BytesIO(base64.b64decode(data)))
    results = model(img, size=640)

    img = np.squeeze(results.render()) #RGB
    # read image as BGR
    img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #BGR
    imgnc = cv2.imencode(".jpg", img_BGR)[1]

    stData = base64.b64encode(imgnc).decode("utf-8")
    b64_src = "data:image/jpeg;base64," 
    emit("server_resp", b64_src+stData)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=3000, type=int, help="port number")
    args = parser.parse_args()
    '''
    model = torch.hub.load(
        "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
    ).autoshape()  # force_reload = recache latest code
    model.eval()
    '''
    app.run(host="0.0.0.0", port=3000)  # debug=True causes Restarting with stat

# Docker Shortcuts
# docker build --tag yolov5 .
# docker run --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --device="/dev/video0:/dev/video0" yolov5
