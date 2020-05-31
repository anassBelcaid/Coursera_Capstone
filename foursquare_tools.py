import requests
import pandas as pd
import numpy as np
import folium
import random
import matplotlib.pyplot as plt
from geopy import Nominatim
from pandas.io.json import json_normalize
import folium

# Credential {{{ #
CLIENT_ID = '4VCZ1KOOIRKHSLQTMSPJML3GXASFVKA35MAV5VZGGHISQZE5' # your Foursquare ID
CLIENT_SECRET = 'CXOCOCPCNAK5K52M3QAATVPA1HFENUWGAENFYT3EXSDDXOPN' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 30
# }}} Credential #
# Fold description {{{ #
def gps_coordinates(description):
    """
    get the gps (latitude, longitude)
    from the description using the foursquare agent
    """
    geolocator = Nominatim(user_agent='foursquare_agent')

    #getting the location
    location = geolocator.geocode(description)
    
    return location.latitude, location.longitude

# }}} Fold description #
# Search for venue category {{{ #
# Search template
#    https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&ll=LATITUDE,LONGITUDE&v=VERSION&query=QUERY&radius=RADIUS&limit=LIMIT

def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']
def venue_query(search_query, position, radius=500, limit=LIMIT):
    """
    search a given venue in position(latitude, longitude)
    """

    #getting the url
    latitude, longitude = position
    url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)

    #getting the json file
    result = requests.get(url).json()
    
    #get the response venues
    venues = result['response']['venues']
    venues = json_normalize(venues)
    filtered_columns = ['name', 'categories'] + [col for col in venues.columns if col.startswith('location.')] + ['id']
    venues = venues.loc[:, filtered_columns]

    #gategories
    venues['categories'] = venues.apply(get_category_type, axis=1)
    return venues

# }}} Search for venue category #
# filter columns for location {{{ #
def filter_columns_locaitons(dataframe):
    """
    keep only columns that include venue name,
    and anything that is associated with location
    """
    filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
    return dataframe.loc[:, filtered_columns]
# }}} filter columns for location #
# category type {{{ #
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']
# }}} category type #
# Map with features {{{ #
def Map_features(position, features = None):
    """
    visualize A map centered around position
    We can get vanues in the features
    """

    map = folium.Map(location= position, zoom_start=13)
    longitude = features['location.lng']
    latitude = features['location.lat']
    labels = features['categories']
    for lat, lng, label in zip(longitude, latitude, labels):
        folium.features.CircleMarker(
                [lat, lng],
                radius=10,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                ).add_to(map)
    return map

# }}} Map with features #
# Explore given an venue {{{ #
def explore_venue(venue_id):
    """
    explore given the id of a venue
    """
    url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID, CLIENT_SECRET, VERSION)

    result = requests.get(url).json()
    return result['response']['venue']


# }}} Explore given an venue #

# search user {{{ #
def search_user(user_id):
    """
    searh a user
    """

    url = 'https://api.foursquare.com/v2/users/{}?client_id={}&client_secret={}&v={}'.format(user_id, CLIENT_ID, CLIENT_SECRET, VERSION) # define URL

    respones = requests.get(url).json()
    user_data = results['response']['user']

    return user_data
# }}} search user #
position = gps_coordinates("Hamria, Meknes, MA")
# results = venue_query("Cafe Calme", position)
# results.to_csv("hamria.csv",index=False)
results = pd.read_csv("hamria.csv")
# function that extracts the category of the venue

# filter the category for each row
id = '50303079e4b0836215df8d5a'
