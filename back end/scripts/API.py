# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 16:52:48 2015

@author: hadrian
"""

import pandas as pd


'''
What we need:
Month
	7 days
	per station/line
	average per half hour

Output:
    day:
    hour: 2-digit hour, 1-digit half-hour
    value: 0 - 2
'''

df = pd.read_csv("/home/hadrian/Desktop/MMDA Traffic /back end/data/01-24/01-24.csv")

def cleanFilterData(data=df, year=2014, month=8, line=0, station=0, bound=0):
    # Function to determine whether time is on the 1st/2nd half of the hour    
    quarterToHalf = lambda x: 0 if (x == 0 or x == 1) else 5    
    # Data Filtering; Select only rows which satisfy criteria
    result = data[(data.year == year) & (data.month == month) & (data.stationID == station) & (data.lineID == line)]
    # Remove unneeded index column     
    result = result.reset_index(drop=True)
    # Apply quarterToHalf to all rows    
    result['half'] = result.apply(lambda row: quarterToHalf(row['quarter']), axis = 1)
    # Remove unneeded columns    
    result = result.drop(['lineID','month','quarter','stationID', 'year'], 1)
    # Index by name of day, hour, half-hour    
    result = result.groupby(['day_name','hour','half'])
    # North or Southbound status
    if bound == 0:
        result = result.statusN.mean().reset_index()
        result.rename(columns={'day_name':'day', 'statusN':'value'}, inplace=True)    
    else:
        result = result.statusS.mean().reset_index()
        result.rename(columns={'day_name':'day', 'statusS':'value'}, inplace=True)    
    # Format hour for Front end
    result.hour = result.hour.map(str) + result.half.map(str)
    result.hour = result.hour.map(int)
    result.day_name = result.day.map(int)
    # Drop unnecessary column    
    result = result.drop(['half'],1)
    return result
