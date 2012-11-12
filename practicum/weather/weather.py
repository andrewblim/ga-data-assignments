# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import datetime
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
import urllib2
import warnings

def temperature_csv(output_filename='temperature.csv',
                    station_url='http://www.nws.noaa.gov/mdl/gfslamp/docs/stations_info_07172012.shtml', 
                    data_url='http://www.nws.noaa.gov/mdl/gfslamp/lavlamp.shtml',
                    verbose=False):
    station_df = station_list(station_url)
    forecast(data_url, station_df, verbose=verbose).to_csv(output_filename, index=False)

def station_list(url):
    
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
            continue  # many stations do not have a TMP line, not a problem
        
        if verbose: print('%s, %s' % (station_code, last_timestamp))
        
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

def colorplot(forecast_data, output_dir='colorplot', verbose=True):
    
    if type(forecast_data) is str:
        data = pd.read_csv('temperature.csv')
    else:
        data = forecast_data
    
    try:
        os.mkdir(output_dir)
    except OSError:
        pass
    
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
        output_filename = '%s.png' % datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d_%H%M')
        
        cbar = fig.colorbar(sc, orientation='vertical')
        cbar.set_label(u'Forecast temperature (\u00B0F)')
        
        fig.savefig(os.path.join(output_dir, output_filename))
        plt.close(fig)
        return cbar
