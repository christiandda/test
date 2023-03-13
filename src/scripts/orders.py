import streamlit as st
import os
import sys
import datetime

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

    # create a sample dataframe
    df = formulas.df_orders()

    # display the dataframe in Streamlit
    st.dataframe(df)

    # Ask the user to input a shop name
    shop_name = st.selectbox("Choose the restaurant",sorted(formulas.names_unique()))
    df_drivers = formulas.df_drivers()
    df_shops = formulas.df_shops()
    closest_driver_id,shop_id = formulas.find_closest_driver(df_drivers, df_shops, shop_name)
    st.write(f"The closest available driver to {shop_name} is {closest_driver_id}")
    st.write(f"Shop id is {shop_id}")

    '''''
    
    '''''
    #shop_namee = st.selectbox("Choose the restaurant",sorted(formulas.names_unique()))

    user_input_order_id  = st.text_input("Orde Id") 
    # The input is then converted into an integer type and stored in the 
    # 'user_input_order_id' variable using the 'int' function. 
    try:
        user_input_order_id = int(user_input_order_id)
    except ValueError:
        st.error("Please enter a valid integer.")

    # If the input is successfully converted to an integer, a success message 
    # is displayed with the integer value using the 'st.success' function.
    if isinstance(user_input_order_id, int):
        st.success(f"You entered the integer: {user_input_order_id}")

    from datetime import datetime

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    restaurant_id=shop_id
    driver_id = closest_driver_id
    user_input_customer_name = st.text_input("customer_name?")
    user_input_customer_address = st.text_input("customer_address?")
    user_input_order_time = st.text_input("Order Time", current_time)
    user_input_delivery_time = st.text_input("Delivery time", current_time)
    user_input_total_amount = float(st.number_input("Total Amount", step=0.01))
    user_input_order_status = st.selectbox("order_status", ["picking up", "Delivering", "Delivered", "Canceled"])

    criteria_selected = user_input_order_status and user_input_order_id

    if st.button('Insert information', disabled=not criteria_selected):
        with st.spinner('Inserting...'):
            formulas.insert_infor_orders(user_input_order_id,user_input_order_status,driver_id,restaurant_id,user_input_customer_name,
                                         user_input_customer_address,user_input_order_time,user_input_delivery_time,user_input_total_amount)
            st.write("Done")

