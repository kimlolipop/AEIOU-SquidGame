import streamlit as st
import base64

css = """<style>
    .center {
        text-align: center; 
        /*color: red; */
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

def run_css():
    st.markdown(css, unsafe_allow_html=True)
