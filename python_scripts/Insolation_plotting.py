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
R1, R2 = 20200501, 20200523
date2 = datelist(R1,R2)
dates = date1 + date2
dates = list(map(str,dates))
data_list = []

for date in dates:
    with open('pickle_files/'+ date + '_0600all_day.pkl','rb') as f:
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
date_array = list(range(0,39))
finaltemp_array_list = []
for d in date_array:
    finaltemp_array_list.append(temp_array_list[d])
      
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

#%% Begins subplotting
index = 0
date_index = 0
time = np.arange(17279)/720

for data_index, data in enumerate(data_list):
    print([data_index,len(data_list)])
    index_list = []
    temp_data = finaltemp_array_list[index]
    insolation_data = insolation_list[index]
    for i in range(17279):
        if data[i,3] < -117 and data[i,3] > -137 and data[i,4] < 3.2 and data[i,4] > 2.8: # finds indexes for power between backazimuth -127 +/- 10 degrees and slowness between 3.2 and 2.8
            index_list.append(i)
    index_list_hours = np.array(index_list)/720
    fig, axes = plt.subplots(6,sharex=True,sharey=False)
    fig.suptitle('Abspow, Relpow, Noise, and Temperature (F) on ' + dates[date_index])
    plt.xlabel('Time (Hours)')
    axes[0].semilogy(index_list_hours,data[index_list,2],'r.',markersize=2) # Plots absolute power
    axes[1].semilogy(index_list_hours,data[index_list,1],'k.',markersize=2) # Plots relative power
    axes[0].set_ylabel('Absolute Power @ 127 degrees +/- 10',fontsize=7)
    axes[1].set_ylabel('Relative Power @ 127 degrees +/- 10',fontsize=7)
    axes[2].plot(time,temp_data[2,:],'b',linewidth=3) # Plots temperature
    axes[2].set_ylabel('Temperature (Fahrenheit)',fontsize=7)
    axes[3].semilogy(time,insolation_data[7,:],'g',linewidth=3) # Plots DNI
    axes[3].set_ylabel('DNI (W/m^2)',fontsize=7)
    axes[4].plot(time,insolation_data[5,:],'c',linewidth=3) # Plots DHI
    axes[4].set_ylabel('DHI W(/m^2)',fontsize=7)
    axes[5].plot(time,insolation_data[6,:],'b',linewidth=3)
    axes[5].set_ylabel('GHI (W/m^2)',fontsize=7)
    plt.savefig('Figures/'+'24hr_subplots/Insolation/' + dates[date_index] + '_24hrs_insolation.jpg',dpi=300)
    plt.clf()
    plt.close()
    date_index = date_index + 1
    index = index + 1
