import streamlit as st
import base64
from playsound import playsound

from src.main import main
from src.main import css



    
### CSS_Style
css.run_css()


### Body
st.markdown('<h5 class="center"> 👾 A E I O U 👾 </h5>', unsafe_allow_html=True)


### Footer
st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open('./src/main/res/image/logo3.png', "rb").read()).decode()}">
    </div>
    """,
    unsafe_allow_html=True)


### Python Code
# playsound('./src/main/res/sound/AEIOU.mp3')
# greenline = st.button('greenline')
# if greenline:
#     playsound('./src/main/res/sound/AEIOU.mp3')
#     greenline = False
    
run = main.run_main()







