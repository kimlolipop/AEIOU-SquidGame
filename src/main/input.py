import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import numpy as np
import tempfile
from sys import getsizeof


# ===============================================
def webcam_input():
    bgsub = cv2.createBackgroundSubtractorKNN(10)
    
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        blur = cv2.GaussianBlur(frame,(5,5),0)
        
        subtraction = bgsub.apply(blur)
        FRAME_WINDOW.image(subtraction)
    else:
        pass

# ===============================================

