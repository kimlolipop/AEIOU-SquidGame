import streamlit as st
from src.main import input

def run_main():
    audio_file = open('./src/main/res/sound/Money.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg',start_time = 2)
    
    open_webcam = input.webcam_input()
