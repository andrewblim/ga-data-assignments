from weather import *
import numpy as np
import pandas as pd
import sys

if __name__ == '__main__':
    
    station_url='http://www.nws.noaa.gov/mdl/gfslamp/docs/stations_info_07172012.shtml'
    data_url='http://www.nws.noaa.gov/mdl/gfslamp/lavlamp.shtml'
    csv_filename='temperature.csv'
    verbose = True
    
    if len(sys.argv) == 1 or sys.argv[1] == 'csv':
        station_df = station_list(station_url)
        forecast(data_url, station_df, verbose=verbose).to_csv(csv_filename, index=False)
    
    if len(sys.argv) == 1 or sys.argv[1] in ['colorplot', 'knn']:
        forecast_data = pd.read_csv(csv_filename)
    
    if len(sys.argv) == 1 or sys.argv[1] == 'colorplot':
        colorplot(forecast_data, 'colorplot', verbose=verbose)
    
    if len(sys.argv) == 1 or sys.argv[1] == 'knn':
        models = knn_forecast_models(forecast_data, 
                                     n_neighbors=1,
                                     warn_on_equidistant=False)
        knn_prediction_grid(forecast_data, models, 
                            np.linspace(35,45,101),
                            np.linspace(-70,-80,101),
                            'grid_1nn',
                            verbose=verbose)
        models = knn_forecast_models(forecast_data, 
                                     n_neighbors=2,
                                     warn_on_equidistant=False)
        knn_prediction_grid(forecast_data, models, 
                            np.linspace(35,45,101),
                            np.linspace(-70,-80,101),
                            'grid_2nn',
                            verbose=verbose)
        models = knn_forecast_models(forecast_data, 
                                     n_neighbors=5,
                                     warn_on_equidistant=False)
        knn_prediction_grid(forecast_data, models, 
                            np.linspace(35,45,101),
                            np.linspace(-70,-80,101),
                            'grid_5nn',
                            verbose=verbose)