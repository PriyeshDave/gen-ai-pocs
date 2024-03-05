import streamlit as st
from PIL import Image

# set the streamlit page theme as light
st.set_page_config(layout="wide", page_title="About Us", page_icon="../Colleague-OnBoarding/assets/images/favicon.png", initial_sidebar_state="expanded")

# Removing the watermark at the bottom
st.markdown('<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>', unsafe_allow_html=True)

with open("./UI/Use Case Descriptions/about_us.txt") as f:
    about_us_text = f.read()
    f.close()

st.markdown("<h1 style='text-align: center; color: black;'> About Us </h1>", unsafe_allow_html=True)
st.markdown("#")
st.markdown(f"<p style='text-align: center; color: black;'>{about_us_text}</p>", unsafe_allow_html=True)

# loading the usecase images. load three images
priyesh_dave = Image.open("./UI/Priyesh Dave.png")
arun_narayanan = Image.open("./UI/Arun Narayanan.png")
manoj_kumar = Image.open("./UI/Manoj Kumar.png")
aniruddha_choudhry = Image.open("./UI/Aniruddha Choudhury.png")

st.markdown('##')
st.markdown("<h2 style='text-align: center; color: black;'> Meet Our Team </h2>", unsafe_allow_html=True)
st.markdown('##')
col1_image, col2_image, col3_image, col4_image = st.columns(4)
col1_image.image(priyesh_dave, use_column_width=True)
col2_image.image(arun_narayanan, use_column_width=True)
col3_image.image(manoj_kumar, use_column_width=True)
col4_image.image(aniruddha_choudhry, use_column_width=True)