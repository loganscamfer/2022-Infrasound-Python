import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
#%% Imports infrasound data
# 24 hour Data
def datelist(r1, r2):
    return [item for item in range(r1, r2+1)]

r1, r2 = 20200415, 20200430
date1 = datelist(r1, r2)
r3, r4 = 20200501, 20200531
r5, r6 = 20200601, 20200611
date2 = datelist(r3,r4)
date3 = datelist(r5,r6)
dates = date1 + date2 + date3
dates = list(map(str,dates))
data_list = []

for date in dates:
    with open('pickle_files/'+ date + '_0600all_day.pkl','rb') as f:
        data_list.append(pickle.load(f))

#%% Calculates Noise
noise_list = []
for data in data_list:
    noise = data[:,2] * ((1-data[:,1])/data[:,1]) # noise = abspower / ((1-relpow)/relpow)
    noise_list.append(noise)
#%% Imports and processes Temperature and Precipitation Data @ Stanely Ranger Station (Fahrenheit)
stanley_data_2020 = np.array(pd.read_csv('imported_data/'+'KSNT_58day.csv',skiprows=[0,1,2,3,4,5,6]))
stanley_temp = stanley_data_2020[:,2]
stanley_precip = stanley_data_2020[:,3]

# Creates an empy list and fills it with each day of 24-hour periods
temp_arrays = np.array_split(stanley_temp,58,axis=0)
precip_arrays = np.array_split(stanley_precip,58,axis=0)
temp_array_list = []
for arrays in temp_arrays:
    temp_array_list.append(np.array([np.repeat(arrays,720,axis=0)]))
for z in range(58):
    a = temp_array_list[z]
    a = np.delete(a,0,axis=1)
    temp_array_list[z] = a
for arrays in temp_array_list:
    arrays.resize(17279)

#%% Imports and processes Insolation data approximately located at infrasound array
insolation_2020 = np.array(pd.read_csv('imported_data/'+'1060595_44.24_-115.07_2020.csv',skiprows=[0,1]))
insolation_2020 = np.delete(insolation_2020, slice(0,15012),axis=0)
insolation_2020 = np.delete(insolation_2020, slice(5616,37647),axis=0)
insolation_split = np.array_split(insolation_2020,39,axis=0)
# Convert split arrays from 10 min intervals to 5-sec time periods.
insolation_list = []
for arrays in insolation_split:
    insolation_list.append(np.array([np.repeat(arrays[:,x],120,axis=0) for x in range(8)]))
for z in range(39):
    a = insolation_list[z]
    a = np.delete(a,0,axis=1)
    insolation_list[z] = a
# NOT YET CONVERTED TO 58 days
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
date_array = list(range(0,39))
finalSWE_array_list = []
for d in date_array:
    finalSWE_array_list.append(swe_array_list[d])
# NOT YET CONVERTED TO 58 days
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
date_array = list(range(0,39))
finalwind_array_list = []
for d in date_array:
    finalwind_array_list.append(wind_array_list[d])
# NOT CONVERTED TO 58 days
#%% Begins subplotting
index = 0
date_index = 0
time = np.arange(17279)/720

for data_index, data in enumerate(data_list):
    print([data_index,len(data_list)])
    index_list = []
    slowness_index = []
    temp_data = temp_array_list[index]
    noise_data = noise_list[index]
    for i in range(17279):
        if data[i,3] < -117 and data[i,3] > -137 and data[i,4] < 3.2 and data[i,4] > 2.8: # finds indexes for power between backazimuth -127 +/- 10 degrees and slowness between 3.2 and 2.8
            index_list.append(i)
    index_list_hours = np.array(index_list)/720
    fig, axes = plt.subplots(4,sharex=True,sharey=False)
    fig.suptitle('Abspow, Relpow, Noise, and Temperature (F) on ' + dates[date_index])
    plt.xlabel('Time after 12:00AM MT (Hours)')
    axes[0].semilogy(index_list_hours,data[index_list,2],'r.',markersize=2) # Plots absolute power
    axes[1].semilogy(index_list_hours,data[index_list,1],'k.',markersize=2) # Plots relative power
    axes[0].set_ylabel('Absolute Power @ 127 degrees +/- 10',fontsize=7)
    axes[1].set_ylabel('Relative Power @ 127 degrees +/- 10',fontsize=7)
    axes[2].semilogy(index_list_hours,noise_data[index_list],'g',linewidth=3) # Plots Noise
    axes[2].set_ylabel('Noise',fontsize=7)
    axes[3].plot(time,temp_data,'b',linewidth=3) # Plots temperature
    axes[3].set_ylabel('Temperature (Fahrenheit)',fontsize=7)
    plt.savefig('Figures/'+'24hr_subplots/' + dates[date_index] + '_24hrs.jpg',dpi=300)
    plt.clf()
    plt.close()
    date_index = date_index + 1
    index = index + 1

