# This script is for producing figures over a 58-day time period (4/15 - 6/11, 2020 )
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd

#%% Imports infrasound data
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

#%% Imports and processes Insolation data approximately located at infrasound array
insolation_2020 = np.array(pd.read_csv('imported_data/'+'1060595_44.24_-115.07_2020.csv',skiprows=[0,1]))
insolation_2020 = np.delete(insolation_2020, slice(0,15012),axis=0)
insolation_2020 = np.delete(insolation_2020, slice(5616,37647),axis=0)
insolation_split = np.array_split(insolation_2020,39,axis=0)

# THIS  NEEDS TO BE CHANGED FOR 58 DAYS
# calculates mean insolation for each day (this inculdes night, where insolation is 0. This will lower the mean insolation and it does not represent the true insolation during the day. 
mean_DNI_list = []
mean_DHI_list = []
mean_GHI_list = []
for arrays in insolation_split:
    mean_DNI = np.mean(arrays[:,7])
    mean_DHI = np.mean(arrays[:,5])
    mean_GHI = np.mean(arrays[:,6])
    
    mean_DNI_list.append(mean_DNI)
    mean_DHI_list.append(mean_DHI)
    mean_GHI_list.append(mean_GHI)

#%% Imports and processes Temperature and Precipitation Data @ Stanely Ranger Station (Fahrenheit)
stanley_data_2020 = np.array(pd.read_csv('imported_data/'+'KSNT_58day.csv',skiprows=[0,1,2,3,4,5,6]))
stanley_temp = stanley_data_2020[:,2]
stanley_precip = stanley_data_2020[:,3]

# Creates an empy list and fills it with each day of 24-hour periods
temp_arrays = np.array_split(stanley_temp,58,axis=0)
precip_arrays = np.array_split(stanley_precip,58,axis=0)

adjusted_temp_arrays = []
adjusted_precip_arrays = []
for arrays in temp_arrays:
    adjusted_temp_arrays.append(arrays[~pd.isna(arrays)]) # Removes nan values
for arrays in precip_arrays:
    adjusted_precip_arrays.append(arrays[~pd.isna(arrays)])

mean_temp_list = []
for arrays in adjusted_temp_arrays:
    total_temp = sum(arrays)
    mean_temp = total_temp / len(arrays)
    mean_temp_list.append(mean_temp)
precip_list = []
for arrays in adjusted_precip_arrays:
    total_daily_precip = sum(arrays)
    precip_list.append(total_daily_precip)
# OUTPUT: 
# mean_temp_list: 58-day list of mean daily temperature
# precip_list: 58-day list of total daily precipitation

#%% Infrasound data processing
points_list = []
power_sum_list = []
median_points = []
for data_index, data in enumerate(data_list):
    print([data_index,len(data_list)])
    index_list = []
    for i in range(17279):
        if data[i,3] < -117 and data[i,3] > -137 and data[i,4] < 3.2 and data[i,4] > 2.8: # finds indexes for power between backazimuth -127 +/- 10 degrees and slowness between 3.2 and 2.8
            index_list.append(i)
    median_points.append(np.median(data[index_list,2]))
    power_sum = sum(data[index_list,2])
    power_sum_list.append(power_sum)
    num_points = len(index_list)
    points_list.append(num_points)
# OUTPUT:
# points_list: 58-day list of number of filtered points detected each day.
# power_sum_list: 58-day list of the sum of absolute powers detected each day.
# median_points: 58-day list of the median absolute power detected each day. 

#%% Plots Sum of Abs Power, # of points detected, Temp, and precip over time.
time = np.arange(58)
start = 3
stop = 4

fig, axes = plt.subplots(4,sharex=True,sharey=False)
fig.suptitle('Power count & Temperature vs Time (04/15-06/11/2020)\n(Cyan highlights indicate Weekends)')
plt.xlabel('Days after 4/15/2020')
for i in range(8):
    axes[0].axvspan(start,stop,color='cyan')
    axes[1].axvspan(start,stop,color='cyan')
    start = start + 7
    stop = stop + 7
axes[0].semilogy(time,power_sum_list,'r',linewidth=2)
axes[0].set_ylabel('Sum of Abs Power',fontsize=7)
axes[1].plot(time,points_list,linewidth=2)
axes[1].set_ylabel('# of points detected',fontsize=7)
axes[2].plot(time,precip_list,'g',linewidth=2)
axes[2].set_ylabel('total daily precip',fontsize = 7)
axes[3].plot(time,mean_temp_list,'b',linewidth=2)
axes[3].set_ylabel('Mean daily temp (F)',fontsize=7)
plt.savefig('Figures/'+'multiday_plots/' + 'Sum of abs power, numpoints, climate',dpi=300)
plt.clf()
plt.close()

#%% Plots median abs power, sum of absolute power, # of points detected, and mean daily temp over time.
start = 3
stop = 4 
time = np.arange(58)

fig, axes = plt.subplots(4,sharex=True,sharey=False)
fig.suptitle('Sum of and median power & Temp vs Time (04/15-06/11/2020)\n(Cyan highlights indicate Weekends)')
plt.xlabel('Days after 4/15/2020')
for i in range(8):
    axes[0].axvspan(start,stop,color='cyan')
    axes[1].axvspan(start,stop,color='cyan')
    axes[2].axvspan(start,stop,color='cyan')
    start = start + 7
    stop = stop + 7
axes[0].semilogy(time,median_points,'r',linewidth=2)
axes[0].set_ylabel('Median Abs power',fontsize=7)
axes[1].semilogy(time,power_sum_list,linewidth=2)
axes[1].set_ylabel('Sum of Abs power',fontsize=7)
axes[2].plot(time,points_list,'g',linewidth=2)
axes[2].set_ylabel('# of points detected',fontsize=7)
axes[3].plot(time,mean_temp_list,'b',linewidth=2)
axes[3].set_ylabel('Mean daily temp (F)',fontsize=7)
plt.savefig('Figures/'+'multiday_plots/' + 'median power, sum of power, numpoints, temp',dpi=300)
plt.clf()
plt.close()
