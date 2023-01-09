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
new_data_list =[]
for d in data_list:
    new_data = np.delete(d,slice(4320,17280),axis=0)
    new_data_list.append(new_data)

#%% Imports and processes Temperature Data @ Stanely Ranger Station (Fahrenheit)
stanley_temp_2020 = pd.read_csv('imported_data/'+'KSNT_temp.csv')
stanely_date_time_temp = np.array(stanley_temp_2020['air_temp_set_1'])

# Creates an empy list and fills it with each day of 24-hour periods
temp_arrays = np.array_split(stanely_date_time_temp,39,axis=0)
mean_temp_list = []
adjusted_temp_arrays = []

for arrays in temp_arrays:
    adjusted_temp_arrays.append(arrays[~np.isnan(arrays)]) # Removes nan values
for arrays in adjusted_temp_arrays:
    total_temp = sum(arrays)
    mean_temp = total_temp / len(arrays)
    mean_temp_list.append(mean_temp)
    
#%% Infrasound data processing (Calculates median power and mean temperature between 12:00-6 MT)
day_index = 0
points_list = []
median_power = list()
for data_index, data in enumerate(new_data_list):
    print([data_index,len(new_data_list)])
    index_list = []
    for i in range(4320):
        if data[i,3] < -117 and data[i,3] > -137 and data[i,4] < 3.2 and data[i,4] > 2.8: # finds indexes for power between backazimuth -127 +/- 10 degrees and slowness between 3.2 and 2.8
            index_list.append(i)
    median_power.append(np.median(data[index_list,2]))
    num_points = sum(index_list)
    points_list.append(num_points)
    day_index = day_index + 1
#%% Plots Number of points & median power & temperature at specific backazimuth for each day (39 days)

time = np.arange(39)
fig, axes = plt.subplots(3,sharex=True,sharey=False)
fig.suptitle('Median power & mean Temperature from 12-6am MT vs Time (04/15-05/23/2020)')
plt.xlabel('Time (Days)')
axes[0].semilogy(time,median_power,'r',linewidth=3)
axes[0].set_ylabel('Median Abs Power',fontsize=7)
axes[1].plot(time,points_list)
axes[1].set_ylabel('# of points detected',fontsize=7)
axes[2].plot(time,mean_temp_list,'b',linewidth=3)
axes[2].set_ylabel('Mean daily Temperature (Fahrenheit)',fontsize=7)

plt.savefig('Figures/'+'multiday_plots/6-12UTC/' + 'Median power vs time',dpi=300)
plt.clf()
plt.close()
