# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 23:59:57 2021

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
    


MTickets=[1425,1100,1100,
         1425,1100,1710,
         1100,1535,1535,
         1535,1200,1535,
         1535,1200,1155,1535]

mtickets=[2*x for x in MTickets]
sigma=calcSigma(mtickets)
value = (gen_random1(4421, 6358))

# value=(4421+6358)/2

rmin=min(mtickets)
rmax=max(mtickets)

rvalue=(gen_random2(rmin,rmax,sigma))


df1=pd.DataFrame(data=np.c_[value,rvalue],columns=['Per Day','Travel'])
df1['Total Budget']=df1['Per Day']+df1['Travel']
df1['Percent Travel']=df1['Travel']*100/df1['Total Budget']
df1['City']='Mumbai'

print(df1[['Per Day','Travel','Percent Travel','Total Budget']].head(-5))


X=df1['Total Budget'].to_numpy().reshape(-1,1)
y=df1['Travel']


X_train,X_test,y_train,y_test=train_test_split(X, y, random_state=0)
r=LinearRegression()
r.fit(X_train,y_train)

filename='Trains_Mumbai.sav'
pickle.dump(r,open(filename,'wb'))