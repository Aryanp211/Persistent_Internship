# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 00:11:43 2021

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



DTickets=[1655,1285,1285,
         1825,1285,1285,
         2010,1285,2010,
         2010,1285,1740,
         1655,1420,1370,
         1785,1420,1785,
         1785,1420,2225,
         965,1615,2225,1785]

dtickets=[2*x for x in DTickets]
sigma=calcSigma(dtickets)
value=gen_random1(4004, 6291)

rmin=min(dtickets)
rmax=max(dtickets)

rvalue=gen_random2(rmin,rmax,sigma)


df3=pd.DataFrame(data=np.c_[value,rvalue],columns=['Per Day','Travel'])
df3['Total Budget']=df3['Per Day']+df3['Travel']
df3['Percent Travel']=df3['Travel']*100/df3['Total Budget']

print(df3)

X=df3['Total Budget'].to_numpy().reshape(-1,1)
y=df3['Travel']


X_train,X_test,y_train,y_test=train_test_split(X, y, random_state=0)
r=LinearRegression()
r.fit(X_train,y_train)

filename='Trains_NewDelhi.sav'
pickle.dump(r,open(filename,'wb'))