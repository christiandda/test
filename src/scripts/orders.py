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




def insert_oders():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style

    st.title('**We add orders**')
    st.markdown(""" <style> .font {
        font-size:40px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.write("We add orders and get a return about which driver will do it")

    # Ask the user to input a shop name
    shop_name = st.selectbox("Choose the restaurant",sorted(formulas.names_unique()))
    df_drivers = formulas.df_drivers()
    df_shops = formulas.df_shops()
    closest_driver_id = formulas.find_closest_driver(df_drivers, df_shops, shop_name)
    st.write(f"The closest available driver to {shop_name} is {closest_driver_id}")
