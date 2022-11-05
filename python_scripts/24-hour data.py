# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:21:16 2022

@author: logan
"""
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
# This script is a predeccesor to power_temp_SWE_subplotting

#%% Imports infrasound data
# 24 Hour Data
dates = ["20200416","20200421","20200423","20200426","20200428","20200430","20200502","20200505","20200506","20200510", "20200511","20200520","20200521","20200522"]
data_list = []

for date in dates:
    with open('pickle_files/'+date + '_0600all_day.pkl','rb') as f:
        data_list.append(pickle.load(f))
         
#%% Plots abs relpow over time
date_index = 0
for data in data_list:
    date = dates[date_index]
    index_list = []

    for i in range(17279):
        if data[i,3] < -117 and data[i,3] > -137: # finds indexes for abs power between backazimuth -127 +/- 10 degrees
            index_list.append(i)
    for index in index_list:
        plt.semilogy(index,data[index,2],'r.',markersize=1)
    plt.savefig('Figures/'+'abspower_24hr/' + date +'_24hrs',dpi=300)
    plt.clf() 
    date_index = date_index + 1
    
#%% Imports and processes Temperature Data @ Banner Summit
bannersummit_temp_2020 = pd.read_csv('imported_data/'+'312_1_YEAR=2020.csv')
banner_date_time_temp = np.array(bannersummit_temp_2020)
banner_date_time_temp = np.delete(banner_date_time_temp, slice(0,2510),axis=0)
banner_date_time_temp = np.delete(banner_date_time_temp, slice(936,6261),axis=0) # removes unneccesary dates from data

# Creates an empy list and fills it with each day of 24-hour periods
split_arrays = []
split_arrays = np.array_split(banner_date_time_temp,39,axis=0)

# Converts split_arrays from 1 hour time periods to 5 sec time periods
# (Each 5 second interval for one hour following the observation hour is filled with the same temp)
temp_array_list = []
for arrays in split_arrays:
    temp_array_list.append(np.array([np.repeat(arrays[:,x],720,axis=0) for x in range(4)]))
for z in range(39):
    a = temp_array_list[z]
    a = np.delete(a,0,axis=1)
    temp_array_list[z] = a
date_array = [1,6,8,11,13,15,17,20,21,25,26,35,36,37]
finaltemp_array_list = []
for d in date_array:
    finaltemp_array_list.append(temp_array_list[d])
      
#%% Imports and processes SWE Data @ Banner Summit
bannersummit_swe_2020 = pd.read_csv('imported_data/'+'312_26_YEAR=2020.csv')
banner_date_time_swe = np.array(bannersummit_swe_2020)
banner_date_time_swe = np.delete(banner_date_time_swe, slice(0,2510),axis=0)
banner_date_time_swe = np.delete(banner_date_time_swe, slice(936,6261),axis=0) # removes unneccesary dates from data

# Creates an empy list and fills it with each day of 3-hour periods
split_arrays = []
split_arrays = np.array_split(banner_date_time_swe,39,axis=0)

# Converts split_arrays from 1 hour time periods to 5 sec time periods 
# (Each 5 second interval for one hour following the observation hour is filled with the same SWE)
swe_array_list = []
for arrays in split_arrays:
    swe_array_list.append(np.array([np.repeat(arrays[:,x],720,axis=0) for x in range(4)]))
for z in range(39):
    a = swe_array_list[z]
    a = np.delete(a,0,axis=1)
    swe_array_list[z] = a
date_array = [1,6,8,11,13,15,17,20,21,25,26,35,36,37]
finalSWE_array_list = []
for d in date_array:
    finalSWE_array_list.append(temp_array_list[d])

