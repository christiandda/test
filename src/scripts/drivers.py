import streamlit as st
import os
import sys

from PIL import Image
import pickle
import requests
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO
import glob
import io
import codecs
from streamlit_option_menu import option_menu

from utils import formulas



PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
data_folder = (PROJECT_ROOT + "/" + "data")
scripts_folder = (PROJECT_ROOT + "/" + "scripts")
files_folder = (scripts_folder + "/" + "files")
saved_models_folder = (data_folder + "/" + "saved_models")
raw_data = (data_folder + "/" + "_raw")
processed_data = (data_folder + "/" + "processed")
images = (PROJECT_ROOT + "/" + "images")




def drivers_info():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style

    st.title('**Drivers Section**')
    st.markdown(""" <style> .font {
        font-size:40px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.write("Here we can see the informacion fo all driver and add new drivers")

    # create a sample dataframe
    df = formulas.df_drivers()

    # display the dataframe in Streamlit
    st.dataframe(df)

    user_input_id  = st.text_input("Drivers Id?")
    user_input_lat  = st.text_input("What is the latitude?")
    user_input_lon = st.text_input("What is the longitude?")
    user_input_disp = st.selectbox("What is the disponibility", ["True", "False"])


    criteria_selected = user_input_id and user_input_lat and user_input_lon and user_input_disp

    if st.button('Insert information', disabled=not criteria_selected):
        with st.spinner('Inserting...'):
            formulas.insert_infor_drivers(user_input_id,user_input_lat,user_input_lon,user_input_disp)
            st.write("Done")
