# Yolov5 Real Time Object Detection model 
![framework](https://img.shields.io/badge/framework-flask-red)
![libraries](https://img.shields.io/badge/libraries-opencv-green)
![models](https://img.shields.io/badge/models-yolov5-yellow)

The Yolov5s pretained model is deployed using flask.
This repo contains example apps for exposing the [yolo5](https://github.com/ultralytics/yolov5) object detection model from [pytorch hub](https://pytorch.org/hub/ultralytics_yolov5/) via a [flask](https://flask.palletsprojects.com/en/1.1.x/) api/app.

The Webapp has a feature to do a realtime detection of Personal Protective Equipment (PPE) and running in cloud.


## Web app
Simple app that enables live webcam detection using pretrained YOLOv5s weights and see real time inference result of the model in the browser.

## Run & Develop locally
Run locally and dev:
* `conda create -n <VENV>`
* `conda activate <VENV>`
* `(<VENV>) $ pip install -r requirements.txt`
* `(<VENV>) $ flask run`

## Docker
```
docker compose up --build
```

## reference
- https://github.com/ultralytics/yolov5
- https://github.com/jzhang533/yolov5-flask
- https://github.com/zyrbreyes/yolov5fish
