import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import torch
import pandas as pd

from src.main.tracker import *
from src.main.sort import *

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./src/main/res/model/yolov5s6.pt')
bgsub = cv2.createBackgroundSubtractorKNN(10)
# tracker = EuclideanDistTracker() ## --> bad
mot_tracker = Sort() ## --> Nice


def webcam_input():
    
    
    option = st.selectbox('Please Select Mode', ('non', 'Subtraction', 'Human_detection'))
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)
   
    
    while run:     
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display
        if option == 'non':
            pass
        elif option == 'Subtraction':
            frame = Subtraction(frame)         
        elif option == 'Human_detection':
            frame = Human_detection(frame)

        FRAME_WINDOW.image(frame)
            
    else:
        pass

def Subtraction(frame):
    
    blur = cv2.GaussianBlur(frame,(5,5),0)
    subtraction = bgsub.apply(blur)
    
    return subtraction


def Human_detection(frame, confidence = 0.6):
    
    # Detector
    frame = cv2.GaussianBlur(frame,(5,5),0)
    detections = []
    results = model(frame)
    d = results.xyxy[0]
    col = ['x1','y1','x2','y2','confidence','class']
    df2 = pd.DataFrame(d, columns=col)
    df2 = df2[df2['class'] == 0.0]
    df2 = df2[df2['confidence'] >= confidence]
    
    for i in range(0, len(df2)):

        x1 = int(df2[['x1']].iloc[i].values[0])
        y1 = int(df2[['y1']].iloc[i].values[0])
        x2 = int(df2[['x2']].iloc[i].values[0])
        y2 = int(df2[['y2']].iloc[i].values[0])
        detections.append([x1, y1, x2, y2])
    

    try:
        boxes_ids = mot_tracker.update(np.array(detections))
        for box_id in boxes_ids:
            x1, y1, x2, y2, id = box_id
            st.write(x1, y1, x2, y2, id)
            cv2.putText(frame, str(id), (int(x1), int(y1) - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)

    except:
        pass
        
    return frame
    
    
    


