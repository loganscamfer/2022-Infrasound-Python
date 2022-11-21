# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 09:48:09 2022

@author: logan
"""
import matplotlib.pyplot as plt
import pickle
import numpy as np

#%% Imports infrasound data (missing 05/04 & 05/08)
# Morning Data (1-4AM MT)
dates = ["20200415","20200416","20200417","20200418","20200419","20200420","20200421","20200422","20200423","20200424","20200425","20200426","20200427","20200428","20200429","20200430","20200501","20200502","20200503","20200505","20200506","20200507","20200509","20200510","20200511","20200512","20200513","20200514","20200515","20200516","20200517","20200518","20200519","20200520","20200521","20200522","20200523"]
data_list = []

for date in dates:
    with open('pickle_files/'+date + '_0700.pkl','rb') as f:
        data_list.append(pickle.load(f))
         
#%% plots backazimuth vs samples for all dates combined
for data in data_list:
    plt.plot(data[:,3],'.')
plt.legend(dates)

#%% plots backazimuth vs absolute relpow for all dates combined
for data in data_list:
    plt.semilogx(data[:,2],data[:,3],".")
plt.legend(dates)

#%% plots backazimuth vs relative relpow for all dates combined
for data in data_list:
    plt.semilogx(data[:,1],data[:,3],".")
plt.legend(dates)

#%%
# plots histogram of backazimuth for all dates combined
for data in data_list:
    hist_1 = np.histogram(data[:,3], bins=24)
    plt.plot(hist_1[1][1:],hist_1[0])
plt.legend(dates)

#%% Plots backazimuth vs samples for each date
for x in range(37):
    sample = data_list[x]
    plt.plot(sample[:,3],".k")
    plt.title(dates[x]+'_0700UTC')
    plt.xlabel('Samples, recorded every 5 sec')
    plt.ylabel('Backazimuth')
    plt.savefig('Figures/'+'backazimuth_vs_samples/morning/' + dates[x]+'_0700')
    plt.clf()
    
#%% Plots backazimuth vs absolute relpow for each date
for x in range(37):
    sample = data_list[x]
    plt.semilogx(sample[:,2],sample[:,3],".k")
    plt.title(dates[x]+'_0700UTC')
    plt.xlabel('Absolute relpow')
    plt.ylabel('Backazimuth')
    plt.savefig('Figures/'+'backazimuth_vs_absolute_pow/morning/' + dates[x]+'_0700')
    plt.clf()
#%% Plots backazimuth vs relative relpow for each date
for x in range(37):
    sample = data_list[x]
    plt.semilogx(sample[:,1],sample[:,3],".k")
    plt.title(dates[x]+'_0700UTC')
    plt.xlabel('Relative relpow')
    plt.ylabel('Backazimuth')
    plt.savefig('Figures/'+'backazimuth_vs_relative_pow/morning/' + dates[x]+'_0700')
    plt.clf()
#%% Plots histogram of backazimuths for each date
for x in range(37):
    sample = data_list[x]
    hist_1 = np.histogram(sample[:,3], bins=24)
    plt.plot(hist_1[1][1:],hist_1[0])
    plt.title(dates[x]+'_0700UTC')
    plt.xlabel('Backazimuth')
    plt.ylabel('Frequency')
    plt.savefig('Figures/'+'histogram_of_backazimuth/morning/' + dates[x]+'_0700')
    plt.clf()
    #%%
