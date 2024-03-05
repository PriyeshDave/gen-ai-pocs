import streamlit as st
from PIL import Image
import os
from st_pages import Page, show_pages, add_page_title

# set the streamlit page theme as light
st.set_page_config(layout="wide", page_title="Gen AI Copilots", page_icon="../Colleague-OnBoarding/assets/images/favicon.png", initial_sidebar_state="expanded")

# Removing the watermark at the bottom
st.markdown('<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>', unsafe_allow_html=True)

############################################################# LOADING THE REQUIRED FILES - START #############################################################
# CSS styling
with open("./CSS/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# loading the banner image
st.markdown("<h1 style='text-align: center; color: black;'>Gen AI Copilots</h1>", unsafe_allow_html=True)
st.markdown('#')
#st.markdown("<p style='text-align: center; color: black; font-family: 'Roboto'; font-size : 50px'> Welcome to Gen AI Copilots </p>", unsafe_allow_html=True)
banner_image = Image.open("./UI/home_page_banner.png")
st.image(banner_image, use_column_width=True)



show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("./pages/About_Us.py", "About Us", "📧"),
        Page("./pages/Data_Copilot.py", "Data Co-Pilot", "📊"),
        Page("./pages/Athena.py", "Athena ", "🤖"),
        Page("./pages/Colleague_Onboarding.py", "Colleague On Boarding", "💼"),
        Page("./pages/Data_Load.py", "Data Up-Load ", "💾"),
    ]
)

# loading the usecase images. load three images
colleague_onboarding = Image.open("./UI/colleague_onboarding.png")
athena = Image.open("./UI/athena.png")
data_copilot = Image.open("./UI/data_copilot.png")

# help laoding the contents of the txt files for each usecase
with open("./UI/Use Case Descriptions/colleague_onboarding.txt") as f:
    colleague_onboarding_text = f.read()
    colleague_onboarding_text = colleague_onboarding_text.strip()
    f.close()
with open("./UI/Use Case Descriptions/athena.txt") as f:
    athena_text = f.read()
    athena_text = athena_text.strip()
    f.close()
with open("./UI/Use Case Descriptions/data_copilot.txt") as f:
    data_copilot_text = f.read()
    data_copilot_text = data_copilot_text.strip()
    f.close()
############################################################# LOADING THE REQUIRED FILES - END #############################################################
    
st.markdown('##')

col1_image, col2_image, col3_image = st.columns(3)
col1_image.image(colleague_onboarding, use_column_width=True)
col2_image.image(athena, use_column_width=True)
col3_image.image(data_copilot, use_column_width=True)

st.markdown('#')
col1_info, col2_info, col3_info= st.columns(3)


col1_info.markdown("<h3 style='text-align: center; color: black;'>Colleague Onboarding</h3>", unsafe_allow_html=True)
col1_info.markdown(f"<p style='text-align: center; color: black;'>{colleague_onboarding_text}</p>", unsafe_allow_html=True)

col2_info.markdown("<h3 style='text-align: center; color: black;'>Athena</h3>", unsafe_allow_html=True)
col2_info.markdown(f"<p style='text-align: center; color: black;'>{athena_text}</p>", unsafe_allow_html=True)

col3_info.markdown("<h3 style='text-align: center; color: black;'>Data Copilot</h3>", unsafe_allow_html=True)
col3_info.markdown(f"<p style='text-align: center; color: black;'>{data_copilot_text}</p>", unsafe_allow_html=True)

st.markdown('##')

col1_button, col2_button, col3_button= st.columns(3)
with col1_button:
    colleague_onboarding_button = st.button("Colleague Onboarding")    
with col2_button:
    athena_button = st.button("Athena")
with col3_button:
    data_copilot = st.button("Data Copilot")

if colleague_onboarding_button:    
    st.switch_page("/pages/Colleague_Onboarding.py")
elif athena_button:
    st.switch_page("/pages/Athena.py")
elif data_copilot:
    st.switch_page("/pages/Data_Copilot.py")






