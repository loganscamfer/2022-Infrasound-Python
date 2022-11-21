# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:44:27 2022

@author: logan
"""
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
import statistics as stats
import scipy
# This script looks at mean power data from 3 hour periods and plots it against climate data from day to day.

#%% Imports infrasound data (missing 05/04 & 05/08)
# Morning Data (1-4AM MT)
dates = ["20200415","20200416","20200417","20200418","20200419","20200420","20200421","20200422","20200423","20200424","20200425","20200426","20200427","20200428","20200429","20200430","20200501","20200502","20200503","20200505","20200506","20200507","20200509","20200510","20200511","20200512","20200513","20200514","20200515","20200516","20200517","20200518","20200519","20200520","20200521","20200522","20200523"]
data_list = []


for date in dates:
    with open('pickle_files/'+date + '_0700.pkl','rb') as f:
        data_list.append(pickle.load(f))

#%% Calculates mean absolute relpow for each date from backazimuths between -132 deg and -122 deg (+/- 5 deg from -127 deg)
# -127 degrees is the backazimuth of the waterfall sound source
# Output is a list: mean_power_list which contains the mean absolute power for each date in dates
mean_power_list = []
sd_power_list = []
for data in data_list:
    index_list = []
    power_list = []
    for i in range(2159):
        if data[i,3] < -122 and data[i,3] > -132:
            index_list.append(i)
    for index in index_list:
        abspower = data[index,2]
        power_list.append(abspower)
    mean_power = stats.mean(power_list)
    sd_power = np.std(power_list)
    mean_power_list.append(mean_power)
    sd_power_list.append(sd_power)
    
# After the "for i" loop is completed, index_list has been filled with points for the first date in data_list. 
# Now we need to run the next for loop to find the mean absolute relpow and append it to mean_power list.
# Next, the "for data" loop will run again, emptying index_list and power_list. 
# Subsequently, it will refill them and calculate the mean abs relpow for the next date and append it to mean_power_list

#%% Imports Streamflow data and removes 05/04 & 05/08 data       
USGS13295000_Discharge = pd.read_excel(r'imported_data/'+'USGS13295000 Discharge Data.xlsx')
discharge = np.array(USGS13295000_Discharge['Discharge (cfs)'])
discharge = np.delete(discharge,19)
discharge = np.delete(discharge, 23)

#%% Imports NOAA temperature data @ Stanley, ID and removes 05/04 & 05/08 data
Stanley_ID_Climate = pd.read_excel(r'imported_data/'+'Stanley, ID Temperature Data.xlsx')
stanley_temp = np.array(Stanley_ID_Climate['Temp Avg'])
stanley_temp = np.delete(stanley_temp,19)
stanley_temp = np.delete(stanley_temp,23)

#%% Imports SNOTEL temperature data @ Banner Summit and removes 05/04 & 05/08 data
banner_summit_meantemp = pd.read_excel(r'imported_data/'+'Idaho SNOTEL Site Banner Summit daily temp.xlsx')
banner_temp = np.array(banner_summit_meantemp['TAVG.D-1 (degC)'])
banner_temp = np.delete(banner_temp,19)
banner_temp = np.delete(banner_temp,23)

#%% Imports Snow Depth @ Banner Summit data and removes 05/04 & 05/08 data
banner_summit_snowdepth = pd.read_excel(r'imported_data/'+'Idaho SNOTEL Site Banner Summit snow depth.xlsx')
snow_depth = np.array(banner_summit_snowdepth['SNWD.I-1 (in)'])
snow_depth = np.delete(snow_depth,19)
snow_depth = np.delete(snow_depth,23)

#%% Plots Discharge vs mean Absolute Relpow @ -127 deg backazimuth +/- 5 deg
discharge_polyfit = np.polyfit(discharge,mean_power_list,1)
discharge_trendline = np.poly1d(discharge_polyfit) # initializes linear regression
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(discharge, mean_power_list) # calculates statistics about regresson
slope_str = str(round(slope,ndigits=4))
r_value_str = str(round(r_value,ndigits=4)) # rounds and converts statistics to strings

plt.plot(discharge,mean_power_list,'.k')
plt.plot(discharge,discharge_trendline(discharge),'r')
plt.suptitle('mean Absolute relpow vs Discharge')
plt.title('Red trendline: Linear regression, slope =' + slope_str + ', R value = ' + r_value_str,fontsize=9)
plt.xlabel('Discharge (cfs) @ USGS13295000 (Valley Creek)')
plt.ylabel('mean Absolute relpow @ -127 degrees +/- 5 degrees')
plt.savefig('Figures/'+'mean_power_plots/' + 'Discharge_vs_absolute_relpow')
plt.clf()

#%% Plots Mean Daily Temp (NOAA source) vs mean Absolute Relpow @ -127 deg backazimuth +/- 5 deg
temp_stanley_polyfit = np.polyfit(stanley_temp,mean_power_list,1)
temp_stanley_trendline = np.poly1d(temp_stanley_polyfit) # initializes linear regression
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(stanley_temp, mean_power_list) # calculates statistics about regresson
slope_str = str(round(slope,ndigits=4))
r_value_str = str(round(r_value,ndigits=4))

plt.plot(stanley_temp,mean_power_list,'.k')
plt.plot(stanley_temp, temp_stanley_trendline(stanley_temp),'r')
plt.suptitle('mean Absolute relpow vs mean daily Temp')
plt.title('Red trendline: Linear regression, slope =' + slope_str + ', R value = ' + r_value_str,fontsize=9)
plt.xlabel('mean daily Temp (Fahrenheit) @ Stanley, ID')
plt.ylabel('mean Absolute relpow @ -127 degrees +/- 5 degrees')
plt.savefig('Figures/'+'mean_power_plots/'+'Stanley_Temperature_vs_absolute_relpow')
plt.clf()

#%% Plots Mean Daily Temp (SNOTEL source) vs mean Absolute Relpow @ -127 deg backazimuth +/- 5 deg
temp_banner_polyfit = np.polyfit(banner_temp,mean_power_list,1)
temp_banner_trendline = np.poly1d(temp_banner_polyfit) # initializes linear regression
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(banner_temp, mean_power_list) # calculates statistics about regresson
slope_str = str(round(slope,ndigits=4))
r_value_str = str(round(r_value,ndigits=4))

plt.plot(banner_temp,mean_power_list,'.k')
plt.plot(banner_temp, temp_banner_trendline(banner_temp),'r')
plt.suptitle('mean Absolute relpow vs mean daily Temp')
plt.title('Red trendline: Linear regression, slope =' + slope_str + ', R value = ' + r_value_str,fontsize=9)
plt.xlabel('mean daily Temp (Celsius) @ Banner Summit SNOTEL')
plt.ylabel('mean Absolute relpow @ -127 degrees +/- 5 degrees')
plt.savefig('Figures/'+'mean_power_plots/'+'Banner_Temperature_vs_absolute_relpow')
plt.clf()

#%% Plots Snow depth vs mean Absolute Relpow @ -127 deg backazimuth +/- 5 deg
snow_polyfit = np.polyfit(snow_depth,mean_power_list,1)
snow_trendline = np.poly1d(snow_polyfit) # initializes linear regression
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(snow_depth, mean_power_list) # calculates statistics about regresson
slope_str = str(round(slope,ndigits=4))
r_value_str = str(round(r_value,ndigits=4))

plt.plot(snow_depth,mean_power_list,'.k')
plt.plot(snow_depth, snow_trendline(snow_depth),'r')
plt.suptitle('mean Absolute relpow vs Snow depth')
plt.title('Red trendline: Linear regression, slope =' + slope_str + ', R value = ' + r_value_str,fontsize=9)
plt.xlabel('Snow depth (in) @ Banner Summit SNOTEL')
plt.ylabel('mean Absolute relpow @ -127 degrees +/- 5 degrees')
plt.savefig('Figures/' +'mean_power_plots/'+'snow_depth_vs_absolute_relpow')
plt.clf()