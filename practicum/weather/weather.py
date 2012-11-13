# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from sklearn.neighbors import KNeighborsRegressor
import datetime
import math
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import urllib2
import warnings

def station_list(url):
    '''Given the url of the NOAA list of stations page, returns a dataframe of
    stations, names, states, and lats/lons. 
    '''
    
    soup = BeautifulSoup(urllib2.urlopen(url))
    d = {'station_code': [],
         'name': [],
         'state': [],
         'latitude': [],
         'longitude': []}
         
    for station_data in soup.find_all('pre'):
        raw_data = re.split(r'\n', station_data.get_text().strip())
        del raw_data[0] # header row
        for line in raw_data:
            d['station_code'].append(line[0:4])
            d['name'].append(line[5:26].strip())
            d['state'].append(line[26:28])
            lat = float(line[28:36])
            if line[36] == 'S': lat = -lat
            d['latitude'].append(lat)
            if line[0:4] == 'KAWM':   # this is wrong in data - should be 90.23W
                d['longitude'].append(-90.23)
            else:
                lon = float(line[37:46])
                if line[46] == 'W': lon = -lon
                d['longitude'].append(lon)
            
    return pd.DataFrame(d)

def forecast(url, station_df, verbose=True):
    '''Given the url of the NOAA's full text bulletin page and a dataframe of
    stations as returned by station_list(), returns a dataframe of times (in 
    UTC terms), temperatures, and lats/lons. 
    '''
    
    soup = BeautifulSoup(urllib2.urlopen(url))
    d = {'utc_timestamp' : [],
         'temperature': [],
         'latitude': [],
         'longitude': []}
         
    raw_data = re.split('\n\s*\n', soup.find('pre').get_text().strip())
    del raw_data[0] # extra '1' row included at start
    station_codes = list(station_df.station_code)
    for raw_block in raw_data:
        
        raw_lines = re.split('\n', raw_block)
        if len(raw_lines) < 3:
            warnings.warn('Possible malformed data block was ignored:\n%s' % raw_block)
            continue
        station_code = raw_lines[0][1:5]
        if station_code not in station_codes:
            raise Exception('%s not in supplied station code list' % station_code)
            
        month = int(raw_lines[0][49:51])
        day = int(raw_lines[0][52:54])
        year = int(raw_lines[0][55:59])
        hour = int(raw_lines[0][61:63])
        minute = int(raw_lines[0][63:65])
        last_timestamp = datetime.datetime(year, month, day, hour, minute)
        
        try:
            utc_row_index = [line[1:4] == 'UTC' for line in raw_lines].index(True)
            utc_row = raw_lines[utc_row_index][5:]
        except ValueError:
            warnings.warn('Station %s had no UTC line and was ignored' % station_code)
            continue
        try:
            tmp_row_index = [line[1:4] == 'TMP' for line in raw_lines].index(True)
            tmp_row = raw_lines[tmp_row_index][5:]
        except ValueError:
            continue  # many stations do not have a TMP line; just skip these
        
        if verbose: print('%s, base time %s' % (station_code, last_timestamp))
        
        for i in range(25):
            hour = int(utc_row[3*i : 3*(i+1)])
            if hour == 99 or hour == 999: # NOAA's weird way of indicating no data...
                timestamp = None
            else:
                if hour <= last_timestamp.hour: # then it rolled to the next day
                    timestamp = last_timestamp + datetime.timedelta(hours=(24 + hour - last_timestamp.hour))
                else:
                    timestamp = last_timestamp + datetime.timedelta(hours=(hour - last_timestamp.hour))
                last_timestamp = timestamp
            temperature = int(tmp_row[3*i : 3*(i+1)])
            if temperature == 99 or temperature == 999: 
                temperature = None  
            station_index = list(station_df.station_code == station_code).index(True)
            station = station_df.ix[station_index]
            d['utc_timestamp'].append(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            d['temperature'].append(temperature)
            d['latitude'].append(station['latitude'])
            d['longitude'].append(station['longitude'])
    
    return pd.DataFrame(d)

def colorplot(forecast_data, output_dir, verbose=True):
    '''Given either a dataframe as returned by forecast() or the corresponding
    csv file, outputs a series of colored scatterplots showing forecasted 
    temperature by location. 
    '''
    
    if isinstance(forecast_data, basestring): data = pd.read_csv(forecast_data)
    else: data = forecast_data
    
    try: os.mkdir(output_dir)
    except OSError: pass
    
    i = 0
    for timestamp in sorted(set(data.utc_timestamp)):
        
        if verbose: print('Graphing %s...' % timestamp)
        histdata = data[np.logical_and(data.utc_timestamp == timestamp,
                                       np.logical_not(np.isnan(data.temperature)))]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        sc = ax.scatter(histdata.longitude, histdata.latitude, 
                        c=histdata.temperature,
                        s=8,
                        cmap=cm.coolwarm,
                        marker='o',
                        edgecolors='none')
        ax.set_title(timestamp)
        ax.set_xlabel('Longitude', size='small')
        ax.set_xticklabels([(u'%.0f\u00B0E' % a if a > 0 else u'%.0f\u00B0W' % -a) for a in ax.get_xticks()], 
                           fontsize='small')
        ax.set_ylabel('Latitude', size='small')
        ax.set_yticklabels([(u'%.0f\u00B0N' % a if a > 0 else u'%.0f\u00B0S' % -a) for a in ax.get_yticks()], 
                           fontsize='small')
        
        cbar = fig.colorbar(sc, orientation='vertical')
        cbar.set_label(u'Forecast temperature (\u00B0F)')
        
        output_filename = '%s.png' % datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d_%H%M')
        fig.savefig(os.path.join(output_dir, output_filename))
        plt.close(fig)

def knn_forecast_models(forecast_data, **kwargs):
    '''Given either a dataframe as returned by forecast() or the corresponding
    csv file, outputs a dictionary mapping timestamps to kNN models. The kwargs
    are passed to sklearn's KNeighborsRegressor. The keys are datetime objects,
    not string representations. 
    '''
    
    if isinstance(forecast_data, basestring): data = pd.read_csv(forecast_data)
    else: data = forecast_data
    
    models = {}
    for timestamp in sorted(set(data.utc_timestamp)):
        index = np.logical_and(data.utc_timestamp == timestamp, 
                               np.logical_not(np.isnan(data.temperature)))
        predictors = data[['latitude', 'longitude']][index]
        response = data.temperature[index]
        timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        models[timestamp] = KNeighborsRegressor(**kwargs).fit(predictors, response)
    
    return models

def knn_predict(model, lat, lon):
    '''Given a knn model and either single lat/lon values or equal-sized lists
    of lats and lons, return predicted values. 
    '''
    
    if '__iter__' in dir(lat) and '__iter__' in dir(lon):
        test_data = pd.DataFrame({'latitude': lat, 'longitude': lon})
    else:
        test_data = pd.DataFrame({'latitude': [lat], 'longitude': [lon]})
    return model.predict(test_data)

def knn_prediction_grid(forecast_data, model_dict, lat_range, lon_range,
                        output_dir, verbose=True):
    
    if isinstance(forecast_data, basestring): data = pd.read_csv(forecast_data)
    else: data = forecast_data

    try: os.mkdir(output_dir)
    except OSError: pass
    
    for timestamp in sorted(set(data.utc_timestamp)):
        
        if verbose: print('Graphing kNN (%s) %s...' % (output_dir, timestamp))
        
        timestamp_as_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        lats = [lat for lat in lat_range for lon in lon_range]
        lons = [lon for lat in lat_range for lon in lon_range]
        predictions = knn_predict(model_dict[timestamp_as_dt], lats, lons)
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        sc = ax.scatter(lons, lats,
                        c=predictions,
                        s=8,
                        cmap=cm.coolwarm,
                        marker='o',
                        edgecolors='none')
        
        inrange_index = np.logical_and(data.utc_timestamp == timestamp,
                                       np.logical_not(np.isnan(data.temperature)))
        inrange_index = np.logical_and(inrange_index, data.latitude >= min(lat_range))
        inrange_index = np.logical_and(inrange_index, data.latitude <= max(lat_range))
        inrange_index = np.logical_and(inrange_index, data.longitude >= min(lon_range))
        inrange_index = np.logical_and(inrange_index, data.longitude <= max(lon_range))
        inrange_data = data[inrange_index]
        sc2 = ax.scatter(inrange_data.longitude, inrange_data.latitude,
                         c=inrange_data.temperature,
                         s=12,
                         cmap=cm.coolwarm,
                         marker='D')
        
        ax.set_title(timestamp)
        ax.set_xlabel('Longitude', size='small')
        ax.set_xticklabels([(u'%.0f\u00B0E' % a if a > 0 else u'%.0f\u00B0W' % -a) for a in ax.get_xticks()], 
                           fontsize='small')
        ax.set_ylabel('Latitude', size='small')
        ax.set_yticklabels([(u'%.0f\u00B0N' % a if a > 0 else u'%.0f\u00B0S' % -a) for a in ax.get_yticks()], 
                           fontsize='small')
    
        cbar = fig.colorbar(sc, orientation='vertical')
        cbar.set_label(u'Forecast temperature (\u00B0F)')
        
        output_filename = '%s.png' % timestamp_as_dt.strftime('%Y%m%d_%H%M')
        fig.savefig(os.path.join(output_dir, output_filename))
        plt.close(fig)