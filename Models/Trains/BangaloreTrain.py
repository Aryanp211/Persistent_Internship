# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 00:12:36 2021

@author: Aryan
"""
import pandas as pd
import scipy.stats as stats
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pickle


def calcSigma(Tickets):
    mu=sum(Tickets)/len(Tickets)
    l1=[pow(abs(mu-x),2)/len(Tickets) for x in Tickets]
    return math.sqrt(sum(l1))

def gen_random1(a,b):
    # a, b = 4421, 6358
    mu = (a+b)/2
    sigma= mu-a
    dist = stats.truncnorm((a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)
    return sorted(dist.rvs(250,random_state=0))



def gen_random2(a,b,sigma):
    # a, b = 4421, 6358
    mu = (a+b)/2
    # sigma= mu-a
    dist = stats.truncnorm((a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)
    return sorted(dist.rvs(250,random_state=0))


BTickets=[2055,1715,1525,
         1720,1540,1810,
         1525,1490,1995,
         2050,2050,2050,
         2190,1875]

btickets=[2*x for x in BTickets]
sigma=calcSigma(btickets)
value=gen_random1(1869,2760)

rmin=min(btickets)
rmax=max(btickets)

rvalue=gen_random2(rmin,rmax,sigma)


df4=pd.DataFrame(data=np.c_[value,rvalue],columns=['Per Day','Travel'])
df4['Total Budget']=df4['Per Day']+df4['Travel']
df4['Percent Travel']=df4['Travel']*100/df4['Total Budget']

# df4['sq']=pow(df4['Total Budget'],2)
print(df4)


X=df4['Total Budget'].to_numpy().reshape(-1,1)
y=df4['Travel']


X_train,X_test,y_train,y_test=train_test_split(X, y, random_state=0)
r=LinearRegression()
r.fit(X_train,y_train)

filename='Trains_Bangalore.sav'
pickle.dump(r,open(filename,'wb'))