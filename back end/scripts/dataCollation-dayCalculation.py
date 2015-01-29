# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 13:43:31 2015

@author: hadrian
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from numpy import *
import datetime
import pyprind

# By Tomohiko Sakamoto 
def calculateDayfromDate(year, month, day):
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    year -= int(month < 3)
    return (year + year/4 - year/100 + year/400 + t[month-1] + day) % 7;


# Access data and create initial dataframe
df = pd.read_csv("/home/hadrian/Desktop/MMDA Traffic /back end/data/collatedOutput/20140724.csv")
# Rename columns
df.columns = ['year','month','day','hour','quarter','lineID','stationID','statusN','statusS']


fndir = "/home/hadrian/Desktop/MMDA Traffic /back end/data/collatedOutput/"
fnsuff=".csv"
startdate=datetime.date(2014,7,25)
one_day=datetime.timedelta(days=1)
nday=184

#Open files and append to data frame
for i in arange(nday):
    thisdate=startdate+one_day*i
    datestr="%4d%02d%02d" % (thisdate.year,thisdate.month,thisdate.day)
    
    new = pd.read_csv(fndir + datestr + fnsuff)
        
    new.columns = ['year','month','day','hour','quarter','lineID','stationID','statusN','statusS']
    
    df = df.append(new, True)

# Add column day_name
df['day_name'] = df.apply(lambda row: calculateDayfromDate(row['year'], row['month'], row['day']), axis = 1)



