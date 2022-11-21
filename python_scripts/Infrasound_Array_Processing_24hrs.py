# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 16:47:53 2022
@author: logan
"""
import matplotlib.pyplot as plt
import obspy
from obspy.signal.array_analysis import array_processing
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import numpy as np
import pickle

client = Client('IRIS')
#%%
def add_inv_coords(st, inv):
    """
    For each trace tr in stream st, adds a 'coordinates' AttribDict to tr.stats using location info
    from an inventory. See application in obspy.signal.array_analysis.array_processing.

    Parameters
    ----------
    st: stream that locations should be added to
    inv: obspy.Inventory or pandas.DataFrame containing locations for all traces in st

    Returns: None, changes st in place
    """
    if type(inv) is obspy.Inventory:
        for tr in st:
            loc = obspy.core.AttribDict(inv.get_coordinates(tr.get_id()))
            tr.stats = obspy.core.Stats({**tr.stats, 'coordinates': loc})
    elif type(inv) is pd.DataFrame:
        for tr in st:
            id = tr.get_id()
            w = np.where(inv.SN == tr.stats.station)[0][0]
            loc = obspy.core.AttribDict(
                {'latitude':inv.loc[w,'lat'],
                 'longitude':inv.loc[w,'lon'],
                 'elevation':0,
                 'local_depth':0}
                )
            tr.stats = obspy.core.Stats({**tr.stats, 'coordinates': loc})
#%%
inv = obspy.read_inventory("XP.PARK.xml")

network_code = 'XP'
station_code = 'PARK'
location_code = '??'
channel_code = 'HDF'

#%% All Day Data (12:00AM-12:00AM)
interval_days = 1
start_time_morning = UTCDateTime("2020-04-15T06:00:00") # Sets start time to  4/15 @6:00 UTC (12:00 MT)
start_time_0 = UTCDateTime("2020-04-15T06:00:00")
start_times = [start_time_0 + i * interval_days * 86400 for i in range(39)]

for start_time_morning in start_times:
    try:
        end_time = start_time_morning + 86400
        st = client.get_waveforms("XP","PARK","??","HDF",start_time_morning,end_time)
        add_inv_coords(st, inv)
        for tr in st: # Removes traces that do not have the full 24 hrs so array_processing is able to run
            if len(tr.data) != 8640001:
                st.remove(tr)
        try:
            Array_1 = array_processing(st,10,0.5,sll_x = -4, slm_x = 4, sll_y = -4, slm_y = 4, 
             sl_s = 0.1, semb_thres = 0, vel_thres = 0, frqlow= 5,
             frqhigh=20, stime = start_time_morning, etime = end_time,
             prewhiten = False, verbose = False, coordsys = 'lonlat',
             timestamp = 'mlabday', method = 0, store = None)
    
            filename = start_time_morning.strftime('%Y%m%d_%H%M') +'all_day.pkl'
            pickle.dump(Array_1,open('pickle_files/'+filename,'wb'))
        except:
            failure_date1 = start_time_morning.strftime('%Y%m%d_%H%M')
            print('Array Processing failed on ' + failure_date1) # error message for array_processing
    except:
        failure_date = start_time_morning.strftime('%Y%m%d_%H%M')
        print('Get waveforms failed on ' + failure_date) # error message for get_waveforms