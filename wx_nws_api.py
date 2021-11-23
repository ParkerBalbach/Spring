
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 12:43:02 2021

@author: dcoladne
"""

import requests
from datetime import datetime, timedelta
from datetime import date
import pandas as pd
import os
import math
import time



def build_url(lon, lat):
    #url = 'https://api.weather.gov/points/{0},{1}/forecast'.format(lat, lon)
    url = 'https://api.weather.gov/points/{0},{1}'.format(lat, lon)
    r = requests.get(url)
    #print(r.json()['properties'])
    #forecast_url = r.json()['properties']['forecast']
    forecast_url = r.json()['properties']['forecastHourly']
    return forecast_url

# url = build_url(-74.3, 40.6)  # ny
url = build_url(-116.3, 43.6)  # boi
r = requests.get(url)

r_json = r.json()

#print([[r_json['properties']['periods'][i]['temperature'], 
#        r_json['properties']['periods'][i]['name'],
#        r_json['properties']['periods'][i]['shortForecast']]
#       for i in range(len(r_json['properties']['periods']))])

#for i in range(len(r_json['properties']['periods'])):
#    print([r_json['properties']['periods'][i]['temperature'], 
#            r_json['properties']['periods'][i]['name'],
#            r_json['properties']['periods'][i]['starttime'],
#            r_json['properties']['periods'][i]['shortforecast']])


# This function takes the weather data and places it into a dataframe
# The function then gets the low and high temperatures based on the hourly forcast
# Lastly the function appends the dataframe onto the dataframe that was passed into the arguments
def append_high_low(in_df):

    url = build_url(-116.3, 43.6)  # boi
    r = requests.get(url)

    r_json = r.json()

    temps_df = pd.DataFrame(columns=['days', 'low', 'high'])

    for i in range(len(r_json['properties']['periods'])):
        cd_string = r_json['properties']['periods'][i]['startTime']
        temp = r_json['properties']['periods'][i]['temperature']
        temps_df = temps_df.append({'days':cd_string, 'low':temp, 'high':temp}, ignore_index=True)

    temps_df.index.name = 'index'
    temps_df['day'] = temps_df['days'].str.slice(start=0,stop=10)
    high_low_temps_df = temps_df.groupby('day').agg({'low':'min', 'high':'max'}).reset_index()
    high_low_temps_df.index.name = 'index'
    high_low_temps_df = high_low_temps_df.drop(labels=0, axis=0)
   
    df = in_df.copy()
    df = df.append(high_low_temps_df, ignore_index=True)

    return df









   


