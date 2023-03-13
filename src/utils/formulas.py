
# Standard library imports
import os # allows access to OS-dependent functionalities
import sys # to manipulate different parts of the Python runtime environment
from math import radians, cos, sin, asin, sqrt
import csv
import re
from pathlib import Path
import streamlit as st

# Libraries go get shop information
import requests  # for HTTP requests
from bs4 import BeautifulSoup # for HTML scrapping 

# Libraries go get shop information
import requests  # for HTTP requests
from bs4 import BeautifulSoup # for HTML scrapping 

# Libraries to Generate random drivers information
import random
import string

import pandas as pd
import numpy as np
import folium

pd.options.mode.chained_assignment = None  # default='warn'


PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
data_folder = (PROJECT_ROOT + "/" + "data")

saved_models_folder = (data_folder + "/" + "saved_models")
raw_data = (data_folder + "/" + "_raw")
processed_data = (data_folder + "/" + "processed")



def df_drivers():
    '''
    This is a Python function called df_shops that reads a CSV file named 
    "drivers_location.csv" located in a directory specified by a variable 
    raw_data. The CSV file is read into a Pandas DataFrame called df_shops.
    Finally, the function returns the df_shops DataFrame.
    '''
    # Creates a df from a csv file
    df_drivers = pd.read_csv(raw_data + "/" + "drivers_location.csv")

    # return the df_drivers DataFrame
    return df_drivers




def df_shops():
    '''
    This is a Python function called df_shops that reads a CSV file named 
    "shops_location.csv" located in a directory specified by a variable 
    raw_data. The CSV file is read into a Pandas DataFrame called df_shops.
    Finally, the function returns the df_shops DataFrame.
    '''
    # Creates a df from a csv file
    df_shops = pd.read_csv(raw_data + "/" + "shops_location.csv")

    # return the df_shops DataFrame
    return df_shops


def df_orders():
    '''
    This is a Python function called df_shops that reads a CSV file named 
    "orders.csv" located in a directory specified by a variable 
    raw_data. The CSV file is read into a Pandas DataFrame called df_shops.
    Finally, the function returns the df_shops DataFrame.
    '''
    # Creates a df from a csv file
    df_orders = pd.read_csv(raw_data + "/" + "orders.csv")

    # return the df_shops DataFrame
    return df_orders


def harvesian_distance(lat1, lon1, lat2, lon2):
    '''
    The code defines a function that calculates the Haversine distance between 
    two points on the Earth's surface, given their latitude and longitude 
    coordinates. The function uses the Haversine formula to calculate the 
    distance assuming a spherical Earth.
    '''
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r



def find_closest_driver(df_drivers, df_shops, shop_name):
    '''
    The code defines a function that finds the closest driver to a given shop, 
    based on the Haversine distance between their respective latitude and longitude 
    coordinates. The function takes two arguments: a list of driver addresses, each 
    represented as a dictionary containing latitude and longitude coordinates, and a 
    shop address represented as a dictionary. The function iterates over each driver's 
    address, calculates the Haversine distance between the driver's address and the 
    shop address using the harvesian_distance() function, and keeps track of the 
    closest driver found so far. The function returns the closest driver's address 
    as a dictionary.
    '''
    # Get the latitude and longitude of the specified shop
    shop_location = df_shops.loc[df_shops['name'] == shop_name, ['latitude', 'longitude']].values.flatten()

    # Get the ID of the shop
    shop_id = df_shops.loc[df_shops['name'] == shop_name, 'id'].iloc[0]

    # Calculate the distance between each driver's location and the shop location using the Haversine formula
    distances = np.array([harvesian_distance(row['lon'], row['lat'], shop_location[1], shop_location[0]) for _, row in df_drivers.iterrows()])

    # Add the distances as a new column in the drivers DataFrame
    df_drivers['distance'] = distances

    # Sort the drivers by their distances to the shop location
    df_drivers.sort_values('distance', inplace=True)

    # Get the ID of the closest available driver to the shop location
    closest_driver_id = df_drivers.loc[(df_drivers['disponibility'] == True) & (df_drivers['distance'] > 0), 'driver_id'].values[0]

    return closest_driver_id,shop_id


def names_unique():
    '''
    Return a list of unique names in the column 'name'
    '''
    shops = df_shops()
    names = shops['name'].unique().tolist()
    return names

def insert_infor_drivers(user_input_id, user_input_disp, user_input_lat=None, user_input_lon=None):
    # Reads the "drivers_location.csv" file and creates a pandas DataFrame object
    df = df_drivers()

    # Check if the driver_id already exists in the DataFrame
    if user_input_id in df['driver_id'].values:
        # Update the existing row with the new information
        if user_input_lat is not None and user_input_lon is not None:
            df.loc[df['driver_id'] == user_input_id, ['disponibility', 'lat', 'lon']] = [ user_input_disp, user_input_lat, user_input_lon,]
        else:
            df.loc[df['driver_id'] == user_input_id, ['disponibility']] = [user_input_disp]
        print(f"Driver with ID {user_input_id} updated successfully.")
        st.write(f"Driver with ID {user_input_id} updated successfully.")
    else:
        # Creates a new row (in the form of a dictionary) to be added to the DataFrame
        new_row = {'driver_id': user_input_id, 'lat': user_input_lat, 'lon': user_input_lon, 'disponibility': user_input_disp}
        # Appends the new row to the DataFrame
        df = df.append(new_row, ignore_index=True)
        print(f"Driver with ID {user_input_id} added successfully.")
        st.write(f"Driver with ID {user_input_id} added successfully.")

    # Writes the updated DataFrame to "drivers_location.csv"
    df.to_csv(raw_data + "/" + "drivers_location.csv", index=False)


def insert_infor_orders(order_id, order_status, driver_id=None, restaurant_id=None, customer_name=None, customer_address=None, order_time=None, delivery_time=None, total_amount=None):
    # Reads the "orders.csv" file and creates a pandas DataFrame object
    df = pd.read_csv(raw_data + "/" + "orders.csv")

    # Check if the order_id already exists in the DataFrame
    if order_id in df['order_id'].values:
        # Update the existing row with the new information
        df.loc[df['order_id'] == order_id, ['driver_id', 'restaurant_id', 'customer_name', 'customer_address', 'order_time', 'delivery_time', 'total_amount', 'order_status']] = [driver_id, restaurant_id, customer_name, customer_address, order_time, delivery_time, total_amount, order_status]
        print(f"Order with ID {order_id} updated successfully.")
        st.write(f"Order with ID {order_id} updated successfully.")
        # Check the order status and call insert_infor_drivers accordingly
        if order_status == "Delivered" or order_status == "Canceled":
            insert_infor_drivers(driver_id, "True")
        else:
            insert_infor_drivers(driver_id, "False")
        st.write(f"Driver with ID {order_id}, status modified.")
    else:
        # Creates a new row (in the form of a dictionary) to be added to the DataFrame
        new_row = {'order_id': order_id, 'driver_id': driver_id, 'restaurant_id': restaurant_id, 'customer_name': customer_name, 'customer_address': customer_address, 'order_time': order_time, 'delivery_time': delivery_time, 'total_amount': total_amount, 'order_status': order_status}
        # Appends the new row to the DataFrame
        df = df.append(new_row, ignore_index=True)
        print(f"Order with ID {order_id} added successfully.")
        st.write(f"Order with ID {order_id} added successfully.")
        # Check the order status and call insert_infor_drivers accordingly
        if order_status == "Delivered" or order_status == "Canceled":
            insert_infor_drivers(driver_id, "True")
        else:
            insert_infor_drivers(driver_id, "False")
        st.write(f"Driver with ID {order_id}, status modified.")

    # Writes the updated DataFrame to "orders.csv"
    df.to_csv(raw_data + "/" + "orders.csv", index=False)