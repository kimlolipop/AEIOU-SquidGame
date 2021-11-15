import streamlit as st
import base64

# st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)

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
