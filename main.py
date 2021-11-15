import streamlit as st
from input import webcam_input, video_input
import base64
import streamlit as st
import css

css = """<style>
.center {
    text-align: center; 
    color: red;
} 

.container {
    display: flex;
    justify-content: center;
}

.logo-img {
   position: fixed;
   bottom: 0;
   width: 2000px;
   padding: 0.5rem;
}


</style>"""

st.markdown(css, unsafe_allow_html=True)

st.markdown('<h1 class="center">👾 Hello World</h1>', unsafe_allow_html=True)

### Footer
st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open('image/logo3.png', "rb").read()).decode()}">
    </div>
    """,
    unsafe_allow_html=True
)





audio_file = open('sound/AEIOU.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg',start_time = 1)


method = st.radio('Go To ->', options=['Webcam', 'Video'])

if method == 'Webcam':
    webcam_input()







