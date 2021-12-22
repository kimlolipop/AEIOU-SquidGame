from src.main import input_frame
import streamlit as st

def run_main():
    audio_file = open('./src/main/res/sound/AEIOU.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg',start_time = 2)
    
    open_webcam = input_frame.webcam_input()
