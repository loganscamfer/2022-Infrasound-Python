import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
#%% Imports infrasound data
# 24 hour Data
dates = ["20200416","20200421","20200423","20200426","20200428","20200430","20200502","20200505","20200506","20200510", "20200511","20200520","20200521","20200522"]
data_list = []

for date in dates:
    with open('pickle_files/'+date + '_0600all_day.pkl','rb') as f:
        data_list.append(pickle.load(f))

#%% Imports and processes Temperature Data @ Stanely Ranger Station (Fahrenheit)
stanley_temp_2020 = pd.read_csv('imported_data/'+'KSNT_temp.csv')
stanely_date_time_temp = np.array(stanley_temp_2020)

# Creates an empy list and fills it with each day of 24-hour periods
split_arrays = []
split_arrays = np.array_split(stanely_date_time_temp,39,axis=0)

# Converts split_arrays from 1 hour time periods to 5 sec time periods
# (Each 5 second interval for one hour following the observation hour is filled with the same temp)
temp_array_list = []
for arrays in split_arrays:
    temp_array_list.append(np.array([np.repeat(arrays[:,x],720,axis=0) for x in range(3)]))
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
    finalSWE_array_list.append(swe_array_list[d])

#%% Imports and processes Wind Data @ Stanley Ranger Station
wind_csv = pd.read_csv('imported_data/'+'KSNT.csv')
stanley_RS_wind = np.array(wind_csv)

# Creates an empy list and fills it with each day
split_arrays = []
split_arrays = np.array_split(stanley_RS_wind,39,axis=0)
# Converts split_arrays from 1 hour time periods to 5 sec time periods 
# (Each 5 second interval for one hour following the observation hour is filled with the same SWE)
wind_array_list = []
for arrays in split_arrays:
    wind_array_list.append(np.array([np.repeat(arrays[:,x],720,axis=0) for x in range(4)]))
for z in range(39):
    a = wind_array_list[z]
    a = np.delete(a,0,axis=1)
    wind_array_list[z] = a
date_array = [1,6,8,11,13,15,17,20,21,25,26,35,36,37]
finalwind_array_list = []
for d in date_array:
    finalwind_array_list.append(wind_array_list[d])

#%% Begins subplotting
index = 0
date_index = 0
time = np.arange(17279)

for data_index, data in enumerate(data_list):
    print([data_index,len(data_list)])
    index_list = []
    slowness_index = []
    temp_data = finaltemp_array_list[index]
    swe_data = finalSWE_array_list[index]
    wind_data = finalwind_array_list[index]
    for i in range(17279):
        if data[i,3] < -117 and data[i,3] > -137 and data[i,4] < 3.2 and data[i,4] > 2.8: # finds indexes for power between backazimuth -127 +/- 10 degrees and slowness between 3.2 and 2.8
            index_list.append(i)

    fig, axes = plt.subplots(5,sharex=True,sharey=False)
    fig.suptitle('Abspow, Relpow, Temperature (F), and SWE (in) on ' + dates[date_index])
    plt.xlabel('Time (5 second increments)')
    axes[0].semilogy(index_list,data[index_list,2],'r.',markersize=2) # Plots absolute power
    axes[1].semilogy(index_list,data[index_list,1],'k.',markersize=2) # Plots relative power
    axes[0].set_ylabel('Absolute Power @ 127 degrees +/- 10',fontsize=7)
    axes[1].set_ylabel('Relative Power @ 127 degrees +/- 10',fontsize=7)
    axes[2].plot(time,temp_data[2,:],'b',linewidth=3) # Plots temperature
    axes[2].set_ylabel('Temperature (Fahrenheit)',fontsize=7)
    axes[3].plot(time,wind_data[2,:],'c') # Plots Wind Speed
    axes[3].set_ylabel('Wind Speed (mph)',fontsize=7)
    axes[4].plot(time,swe_data[3,:],'g',linewidth=3) # Plots SWE
    axes[4].set_ylabel('Snow Water Equivalent (inches)',fontsize=7)
    plt.savefig('Figures/'+'24hr_subplots/' + dates[date_index] + '_24hrs.jpg',dpi=300)
    plt.clf()
    plt.close()
    date_index = date_index + 1
    index = index + 1

