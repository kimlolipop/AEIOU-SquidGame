import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import numpy as np
import tempfile
from sys import getsizeof


# ===============================================Ui
def webcam_input():
    st.title("Webcam Live Feed")
#     webrtc_streamer(key="example")
    
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    else:
        st.write('Stopped')
    
    
def video_input(c_upload):

    f = st.file_uploader("Upload file")
#     if f is not None:
    video = []
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(f.read())
    cap = cv2.VideoCapture(tfile.name)

    # Get the frames per second
    fps = cap.get(cv2.CAP_PROP_FPS)
    st.write('FPS: ', fps)

    # Get the total numer of frames in the video. value same as image frame
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    st.write('Frame-count: ', frame_count)

    #Time of video(sec)
    duration = frame_count / fps
    st.write('Duration: ', duration)

    # sent to read
    video, no_frame = read_video(cap, video)
    c_upload = True
#     else: 
#         video = []
#         frame_count = 10
#         c_upload = False
#         no_frame = 10
        
    return video, frame_count, c_upload, no_frame
    

    
def read_video(cap, video):
#     stframe = st.empty()
    i = 0
    no_frame = 0
    bgsubknn = cv2.createBackgroundSubtractorKNN()
    while cap.isOpened():
        i = i + 1
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         im = bgsubknn.apply(frame)
        
        if i == 10:
            i = 0
            no_frame = no_frame + 1
            video.append(im)
            
            #show
#             stframe.image(im)

    return video, no_frame

# ===============================================Ui

