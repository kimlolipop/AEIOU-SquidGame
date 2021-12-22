import streamlit as st

from streamlit_webrtc import (
    ClientSettings,
    VideoProcessorBase,
    webrtc_streamer,
)

import cv2
import numpy as np
import torch
import pandas as pd
import av

from src.main.sort import *

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
'''
    --> Function AEIOU_game ใช้สำหรับ logic เกมส์ flow chart คร่าวๆ
    
    
    --> Function webcam_input ใช้สำหรับ control mode webcam และรับค่าจากกล้อง
    --> Function Human_detection ใช้ detect คน + tracker
    --> Function Subtraction ใช้ทำ Subtraction
    

'''


model = torch.hub.load('ultralytics/yolov5', 'custom', path='./src/main/projects/human_detection_Yolov5/model/yolov5s6.pt') # YoloV5 PRetrain

bgsub = cv2.createBackgroundSubtractorKNN(10) 
mot_tracker = Sort() ## --> realtime tracker


# Setting for online connect
WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
)


def webcam_input():
    
    option = st.selectbox('Please Select Mode', ('non', 'Subtraction', 'Human_Detector', 'AEIOU_Game'))
    
    class OpenCVVideoProcessor(VideoProcessorBase):
        type: Literal["Default", "Subtraction", "Human_Detector", "Face_Detector"]

        def __init__(self) -> None:
            self.type = "Default"

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")

            if self.type == "Default":
                pass
            elif self.type == "Human_Detector":
                img = cv2.GaussianBlur(img,(5,5),0)
                img = Human_detection(img)
                
            elif self.type == "Subtraction":
                img = cv2.GaussianBlur(img,(5,5),0)
                img = cv2.cvtColor(Subtraction(img),cv2.COLOR_GRAY2BGR)
                
                        
            return av.VideoFrame.from_ndarray(img, format="bgr24")
    
 
    webrtc_ctx = webrtc_streamer(
        key="opencv-filter",
        client_settings=WEBRTC_CLIENT_SETTINGS,
        video_processor_factory=OpenCVVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    
    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.type = option
    
    

def Subtraction(frame):
    
    subtraction = bgsub.apply(frame)
    
    return subtraction


def Human_detection(frame, confidence = 0.6):
    
    # Detector
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
    
    
    # Tracker by Sort
    try:
        boxes_ids = mot_tracker.update(np.array(detections))
        for box_id in boxes_ids:
            x1, y1, x2, y2, id = box_id
            cv2.putText(frame, str(id), (int(x1), int(y1) - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)

    except:
        pass
        
    return frame



def AEIOU_game(frame):
        
    # Detect + sort
    # ======Red Line --> ห้ามขยับ
    # --> crop obj to subtrack 
        # if move change object box color
    # --> Action button for start Green line
    
    
    # ======Green Line --> ขยับได้ Render เพลง AEIOU
    # --> reset status
    # --> Random select AEIOU music [แต่ละเพลงความยาวไม่เท่ากัน]

    pass
    