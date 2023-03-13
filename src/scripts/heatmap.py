import streamlit as st
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import MarkerCluster


from folium.plugins import HeatMapWithTime
from utils import formulas


import seaborn as sns


from geopy.geocoders import Nominatim




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




def heatmap_info():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style

    st.title('**Real Time Heatmap**')
    st.markdown(""" <style> .font {
        font-size:40px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.write("We can see in real time the HOT (more busy) areas")



    # Load the dataframes
    shop_df = formulas.df_shops()
    orders_df = formulas.df_orders()

    # Merge the two dataframes on the restaurant_id column
    merged_df = pd.merge(shop_df, orders_df, left_on='id', right_on='restaurant_id')
    st.dataframe(merged_df)


    # Load data with latitude and longitude columns
    df = merged_df

    # Create map
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=15)

    # Add markers
    heat_data = [[row["latitude"], row["longitude"]] for index, row in df.iterrows()]
    from folium.plugins import HeatMap
    HeatMap(heat_data).add_to(m)

    # Display map
    folium_static(m)
