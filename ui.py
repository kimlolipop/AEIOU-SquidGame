import streamlit as st

# from data import *
from input import webcam_input, video_input

st.title("Neural Style Transfer")
st.sidebar.title('Navigation')
method = st.sidebar.radio('Go To ->', options=['Webcam', 'Video', 'test'])
st.sidebar.header('Options')



# status/ state
if 'c_upload' not in st.session_state: # create state name --> cnt
    st.session_state.c_upload = False
    
if 'video' not in st.session_state: # create state name --> cnt
    st.session_state.video = []
    
if 'no_frame' not in st.session_state: # create state name --> cnt
    st.session_state.no_frame = 0
        
    
    
c_upload = False
st.write("upload 1: " + str(st.session_state.c_upload))

if method == 'Video':
  
    if st.session_state.c_upload == False:
        video = st.session_state.video
        st.write(len(video))
        st.write("upload 2: " + str(st.session_state.c_upload))
        c_upload = st.session_state.c_upload
        video, frame_count, st.session_state.c_upload, no_frame = video_input(c_upload)
        
        st.session_state.video = video
        st.session_state.no_frame = no_frame
        st.write("no of video: " + str(st.session_state.c_upload))

    if st.session_state.c_upload == True:
        st.write("no frame: ", len(st.session_state.video))
        if len(st.session_state.video) > 0:
            
            st.write("upload 3: " + str(st.session_state.c_upload))
            values = st.slider( 'Select a range of values',0, int(st.session_state.no_frame) - 1, 1)
            st.write('Values:', values)
            
            stframe = st.empty()
            stframe.image(st.session_state.video[values])

#     st.write('f')
    
elif method == 'test':
    st.title('Counter Example')

    if 'cnt' not in st.session_state: # create state name --> cnt
        st.session_state.cnt = 0

    increment = st.button('Increment')    
    if increment:
        st.session_state.cnt += 1

    decrement = st.button('Decrement')
    if decrement:
        st.session_state.cnt -= 1

    st.write('Count = ', st.session_state.cnt)
    
    if st.session_state.cnt == 5:
        st.write('finish')
    
else:
    webcam_input()
    