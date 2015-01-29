# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 17:44:00 2015

@author: hadrian
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
from numpy import *
import datetime

'''
What we need:
Month
	7 days
	per station/line
	average per half hour

Output:
    day:
    hour:
    value:
'''

# Access data and create initial dataframe
df = pd.read_csv("/home/hadrian/Desktop/MMDA Traffic /back end/data/01-24/01-24.csv")

# alpha 1
### Remove invalid data
#invalid = df[df.statusN < 0] + df[df.statusS < 0]
#valid = df.drop(invalid.index.values)
#
#valid.to_csv('01-24.csv', index=False)

# Convert to datetime
#def toDate(year,month,day):
#    return datetime.date(year,month,day)
#
#valid['date'] = valid.apply(lambda row: toDate(row['year'],row['month'],row['day']), axis = 1)
## remove unnecessary columns
#del valid['year']
#del valid['month']
#del valid['day']

## Process lines 
## For line 0
#lineZero = df[df.lineID==0]
#stations = pd.unique(lineZero.stationID)

## alpha 2
#del df[df.columns[0]]

## Get df for specific line, station and month
#def perMonthLineStation(data=valid, year=2014, month=8, line=0, station=0):
#    result = data[(data.year == year) & (data.month == month) & (data.stationID == station) & (data.lineID == line)]     
#    result = result.reset_index(drop=True)
#    return result
#
#
#def perDay(data, day_name):
#    result = data[(data.day_name == day_name)]
#    result = result.reset_index(drop=True)
#    return result
#
#quarterToHalf = lambda x: 0 if (x == 0 or x == 1) else 5
#
#
#test = perMonthLineStation()
## Create new column 'Half' hour
#test['half'] = test.apply(lambda row: quarterToHalf(row['quarter']), axis = 1)
#
## Delete irrelevant columns
#test = test.drop(['lineID','month','quarter','stationID', 'year'], 1)
#
## DataFrame Groupby
#grouped = test.groupby(['day_name','hour','half'])
#
## Mean of statusN per day_name and hour
#mean = grouped.statusN.mean().reset_index()

# Reset index 
#df.reset_index(drop=True)

