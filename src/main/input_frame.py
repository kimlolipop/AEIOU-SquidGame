import streamlit as st
from playsound import playsound

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
from random import randrange, uniform

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

if 'model' not in st.session_state:
    st.session_state.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./src/main/projects/human_detection_Yolov5/model/yolov5s6.pt') 
    
bgsub = cv2.createBackgroundSubtractorKNN(1) 
mot_tracker = Sort() ## --> realtime tracker



# Setting for online connect
# WEBRTC_CLIENT_SETTINGS = ClientSettings(
#     rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
#     media_stream_constraints={"video": True, "audio": False},
# )

def webcam_input():
    st.title("Webcam Live Feed")
    option = st.selectbox('Please Select Mode', ('non', 'Subtraction', 'Human_Detector', 'AEIOU_Game'))
    
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)
   
    
    #setup AEIOU
    if 'count' not in st.session_state:
        st.session_state.count = 0
    id_dead = []
    music_lst = ['AEIOU_01.mp3','AEIOU_02.mp3','AEIOU_03.mp3','AEIOU_04.mp3','AEIOU_05.mp3','AEIOU_06.mp3','AEIOU_07.mp3','AEIOU_08.mp3','AEIOU_09.mp3','AEIOU_10.mp3']
    path = './src/main/res/sound/'
    


    
    while run:
        _, frame = camera.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if option == "non":
            pass
        elif option == "Human_Detector":
            img = cv2.GaussianBlur(img,(5,5),0)
            img = Human_detection(img)

        elif option == "Subtraction":
            img = cv2.GaussianBlur(img,(5,5),0)

        elif option == 'AEIOU_Game':
            st.session_state.count += 1
            img = cv2.GaussianBlur(img,(5,5),0)
            img = cv2.GaussianBlur(img,(5,5),0)
            img, id_dead = AEIOU_game(img, id_dead, st.session_state.count)
            
            try:
                greenline = st.button('greenline')
            except:
                pass
            

            if greenline:
                no = randrange(0, 10)
                print(music_lst[no])
                playsound(path + music_lst[no])
                st.session_state.count = 0
                greenline = False
                

                
                
                
        FRAME_WINDOW.image(img)
    else:
        pass
        
    cv2.destroyAllWindows()
        


    
    

def Subtraction(frame):
    
    subtraction = bgsub.apply(frame)
    
    return subtraction


def Human_detection(frame, confidence = 0.6):
    
    # Detector
    detections = []
    results = st.session_state.model(frame)
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






def AEIOU_game(frame, id_dead, count):
    # ======Red Line --> ห้ามขยับ
    #setup
    confidence =  0.6
    blue = (0,0,255)
    red = (255,0,0)
    Threshold = 1579346
    Delay_detect = 6
    
    # --> crop obj to subtrack 
    subtract = Subtraction(frame)
    
    # --> Detect + sort
    detections = []
    results = st.session_state.model(frame)
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
        boxes_ids = np.array(boxes_ids,dtype=int)
        for box_id in boxes_ids:
            x1, y1, x2, y2, id = box_id
            

            subtraction_crop = subtract[y1:y1+(y2-y1), x1:x1+(x2-x1)]
            flow_check = subtraction_crop.sum()
            print(flow_check)
            
            if ((flow_check > Threshold) | (id in id_dead)) and count > Delay_detect:
                
                if id not in id_dead: # --> New ID
                    id_dead.append(id)
                
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), red, 3)
                cv2.putText(frame, str(id), (x1, y1 - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), blue, 3)

    except:
        print('error')
        pass
    
    
    
    frame_show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # cv2.imshow('detect', frame_show)
    cv2.imshow('Subtract', subtract)
    cv2.waitKey(25)
    
    
  

    
    return frame, id_dead

    
    
    
    
    
    
    
# def webcam_input2():
    
#     option = st.selectbox('Please Select Mode', ('non', 'Subtraction', 'Human_Detector', 'AEIOU_Game'))

            
#     class OpenCVVideoProcessor(VideoProcessorBase,):
#         type: Literal["Default", "Subtraction", "Human_Detector", "Face_Detector"]
        

#         def __init__(self) -> None:
#             self.type = "Default"

#         def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
#             img = frame.to_ndarray(format="bgr24")

#             if self.type == "Default":
#                 pass
#             elif self.type == "Human_Detector":
#                 img = cv2.GaussianBlur(img,(5,5),0)
#                 img = Human_detection(img)
                
#             elif self.type == "Subtraction":
#                 img = cv2.GaussianBlur(img,(5,5),0)
#                 img = cv2.cvtColor(Subtraction(img),cv2.COLOR_GRAY2BGR)
                
#             elif self.type == 'AEIOU_Game':
#                 img = cv2.GaussianBlur(img,(5,5),0)
#                 img = AEIOU_game(img)

                
             
#             return av.VideoFrame.from_ndarray(img, format="bgr24")
    
 
#     webrtc_ctx = webrtc_streamer(
#         key="opencv-filter",
#         # client_settings=WEBRTC_CLIENT_SETTINGS,
#         video_processor_factory=OpenCVVideoProcessor,
#         media_stream_constraints={"video": True, "audio": False},
#         async_processing=True,
#     )
    
    
#     if webrtc_ctx.video_processor:
#         webrtc_ctx.video_processor.type = option
        
#     cv2.destroyAllWindows()