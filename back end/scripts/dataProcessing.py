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


data = pd.read_csv("/home/hadrian/collatedOutput/20140724.csv")


# By Tomohiko Sakamoto 

def calculateDayfromDate(year, month, day):
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    year -= int(month < 3)
    return (year + year/4 - year/100 + year/400 + t[month-1] + day) % 7;


''' Collate all files into one dataframe 

fndir = "/home/hadrian/collatedOutput/"
fnsuff=".csv"
startdate=datetime.date(2014,7,25)
one_day=datetime.timedelta(days=1)
nday=184


#Open files and append to data frame
for i in arange(nday):
    thisdate=startdate+one_day*i
    datestr="%4d%02d%02d" % (thisdate.year,thisdate.month,thisdate.day)
    new = pd.read_csv(fndir + datestr + fnsuff)
    data = data.append(new, True)

'''
 