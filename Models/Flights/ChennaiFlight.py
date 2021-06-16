# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 17:30:03 2021

@author: Aryan
"""


# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 00:10:48 2021

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


CTickets=[2676,4246,5574,5742,5884,6135,6771,2155,2312]

ctickets=[2*x for x in CTickets]
sigma=calcSigma(ctickets)
value=gen_random1(1968, 2667)

rmin=min(ctickets)
rmax=max(ctickets)

rvalue=(gen_random2(rmin,rmax,sigma))


df2=pd.DataFrame(data=np.c_[value,rvalue],columns=['Per Day','Travel'])
df2['Total Budget']=df2['Per Day']+df2['Travel']
df2['Percent Travel']=df2['Travel']*100/df2['Total Budget']

print(df2.head(-5))



X=df2['Total Budget'].to_numpy().reshape(-1,1)
y=df2['Travel']


X_train,X_test,y_train,y_test=train_test_split(X, y, random_state=0)
r=LinearRegression()
r.fit(X_train,y_train)
filename='Flights_Chennai.sav'
pickle.dump(r,open(filename,'wb'))