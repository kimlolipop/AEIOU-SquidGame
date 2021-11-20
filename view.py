import streamlit as st
import base64
from playsound import playsound

from src.main import input
from src.main import css






css.run_css()

st.markdown('<h1 class="center"> 👾 A E I O U 👾 </h1>', unsafe_allow_html=True)


### Footer
st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open('./src/main/res/image/logo3.png', "rb").read()).decode()}">
    </div>
    """,
    unsafe_allow_html=True
)







audio_file = open('./src/main/res/sound/AEIOU.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg',start_time = 2)

input.webcam_input()








