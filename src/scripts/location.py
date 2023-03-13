import streamlit as st
import os
import sys
import folium
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




def location_info():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style

    st.title('**ON Stream Location**')
    st.markdown(""" <style> .font {
        font-size:40px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.write("We can see in real time the location of the drivers")
    st.markdown('<h1>Map of Available Drivers</h1>', unsafe_allow_html=True)

    # Load the driver data
    df_drivers = formulas.df_drivers()

    # Filter the available drivers
    available_drivers = df_drivers[df_drivers['disponibility'] == True]

    '''
    FIRST MAPA
    '''
    # Create a Folium map centered on the mean location of available drivers
    m = folium.Map(location=[available_drivers.lat.mean(), available_drivers.lon.mean()], zoom_start=3, control_scale=True)

    # Add a marker cluster for the available drivers
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers for each available driver
    for i, row in available_drivers.iterrows():
        # Create a marker with an iframe in the popup
        popup_html = f"<b>Driver ID:</b> {row['driver_id']}<br><b>Availability:</b> {row['disponibility']}"
        iframe_html = folium.IFrame(popup_html, width=200, height=100)
        popup = folium.Popup(iframe_html, max_width=2650)
        marker = folium.Marker(location=[row['lat'], row['lon']], popup=popup, icon=folium.Icon(color='green', icon='car', prefix='fa'))
        marker_cluster.add_child(marker)

    # Display the map in Streamlit using folium_static
    folium_static(m)



    '''
    Segundo MAPA
    '''
    st.markdown('<h1>Map of NOT Available Drivers</h1>', unsafe_allow_html=True)
    # Create a Folium map centered on the mean location of available drivers

    # Load the driver data
    df_drivers = formulas.df_drivers()

    # Filter the available drivers
    available_drivers = df_drivers[df_drivers['disponibility'] == False]

    # Create a Folium map centered on the mean location of available drivers
    m = folium.Map(location=[available_drivers.lat.mean(), available_drivers.lon.mean()], zoom_start=3, control_scale=True)

    # Add a marker cluster for the available drivers
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers for each available driver
    for i, row in available_drivers.iterrows():
        # Create a marker with an iframe in the popup
        popup_html = f"<b>Driver ID:</b> {row['driver_id']}<br><b>Availability:</b> {row['disponibility']}"
        iframe_html = folium.IFrame(popup_html, width=200, height=100)
        popup = folium.Popup(iframe_html, max_width=2650)
        marker = folium.Marker(location=[row['lat'], row['lon']], popup=popup, icon=folium.Icon(color='green', icon='car', prefix='fa'))
        marker_cluster.add_child(marker)

    # Display the map in Streamlit using folium_static
    folium_static(m)
    

