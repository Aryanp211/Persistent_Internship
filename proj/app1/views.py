from django.shortcuts import render
from . import trains_df as tr
from . import flights_df as fl
import numpy as np
import logging
import pickle
# Create your views here.


stncode={'Mumbai':'CSMT','New Delhi':'NDLS','Chennai':"MAS","Bangalore":'SBC','Nagpur':'NGP'}
aircode={'Mumbai':'BOM','New Delhi':'DEL','Chennai':"MAA","Bangalore":'BLR','Nagpur':'NAG'}


def home(request):
    return render(request,"app1/home.html")


def predictor(source,destination,budget,transport):
    code={'Mumbai':1,'Chennai':2,'New Delhi':3,'Bangalore':4}
    
    F_Mumbai = pickle.load(open('Flights_Mumbai.sav', 'rb'))
    T_Mumbai = pickle.load(open('Trains_Mumbai.sav', 'rb'))
    F_Chennai = pickle.load(open('Flights_Chennai.sav', 'rb'))
    T_Chennai = pickle.load(open('Trains_Chennai.sav', 'rb'))   
    F_NewDelhi = pickle.load(open('Flights_NewDelhi.sav', 'rb'))
    T_NewDelhi = pickle.load(open('Trains_NewDelhi.sav', 'rb'))    
    F_Bangalore = pickle.load(open('Flights_Bangalore.sav', 'rb'))
    T_Bangalore = pickle.load(open('Trains_Bangalore.sav', 'rb'))
    
    
    
    if destination=='Mumbai':
    
        if transport=='f':   
            prediction=F_Mumbai.predict(np.array(budget).reshape(1,-1))[0]
            return prediction
        elif transport=='t':
            prediction=T_Mumbai.predict(np.array(budget).reshape(1,-1))[0]
            return prediction
        else:
            predictionF=F_Mumbai.predict(np.array(budget).reshape(1,-1))[0]
            predictionT=T_Mumbai.predict(np.array(budget).reshape(1,-1))[0]
            return [predictionF,predictionT]


    if destination=='Chennai':
    
        if transport=='f':   
            prediction=F_Chennai.predict(np.array(budget).reshape(1,-1))[0]
            return prediction
        elif transport=='t':
            prediction=T_Chennai.predict(np.array(budget).reshape(1,-1))[0]
            return prediction
        else:
            predictionF=F_Chennai.predict(np.array(budget).reshape(1,-1))[0]
            predictionT=T_Chennai.predict(np.array(budget).reshape(1,-1))[0]
            return [predictionF,predictionT]



    if destination=='New Delhi':
    
        if transport=='f':   
            prediction=F_NewDelhi.predict(np.array(budget).reshape(1,-1))[0]
            return prediction
        elif transport=='t':
            prediction=T_NewDelhi.predict(np.array(budget).reshape(1,-1))[0]
            return prediction
        else:
            predictionF=F_NewDelhi.predict(np.array(budget).reshape(1,-1))[0]
            predictionT=T_NewDelhi.predict(np.array(budget).reshape(1,-1))[0]
            return [predictionF,predictionT]

    if destination=='Bangalore':
    
        if transport=='f':   
            prediction=F_Bangalore.predict(np.array(budget).reshape(1,-1))[0]
            return prediction
        elif transport=='t':
            prediction=T_Bangalore.predict(np.array(budget).reshape(1,-1))[0]
            return prediction
        else:
            predictionF=F_Bangalore.predict(np.array(budget).reshape(1,-1))[0]
            predictionT=T_Bangalore.predict(np.array(budget).reshape(1,-1))[0]
            return [predictionF,predictionT]



def result(request):
    origin=request.POST['origin']
    destination=request.POST['destination']
    from_date=request.POST['from_date']
    to_date=request.POST['to_date']
    budget=request.POST['budget']
    transport=request.POST['transport']
    year=from_date[0:4]
    month=from_date[5:7]
    day=from_date[8:10]

    flightDate=day+'/'+month+'/'+year
    TrainDate=year+month+day
    logging.warning('DATEEEEEEEEEEEEEE',type(from_date))
    mxval=predictor(origin,destination,budget,transport)
    logging.warning("XXXXXXXXXX",mxval)
    
    logging.warning('ACCCCCCCCCCCCCCCCCCCCCCCCCCC',mxval)
   
    
    if transport=='f':
        df1=fl.flight_call(aircode[origin],aircode[destination],flightDate)
        logging.warning('SSSSSSSSSSS',df1)
        df1=df1[df1['Cost']<=mxval]

        l=[]
        for i in range(len(df1)):
            l.append(df1.iloc[i].values)        
        return render(request,'app1/display.html',{'f':True,'t':False,'ft':False,'df1':df1,'values':l, 'empty':len(df1)==0})
    
    if transport=='t':
        df1=tr.train_call(destination,stncode[destination],origin,stncode[origin],TrainDate)
        df1=df1[df1['Cost']<=mxval]
        l=[]
        for i in range(len(df1)):
            l.append(df1.iloc[i].values)
        return render(request,'app1/display.html',{'f':False,'t':True,'ft':False,'df1':df1,'values':l, 'empty':len(df1)==0})

    if transport=='ft':
        df1=fl.flight_call(aircode[origin],aircode[destination],flightDate)
        df1=df1[df1['Cost']<=mxval[0]]
        logging.warning('f1 over')
        df2=tr.train_call(destination,stncode[destination],origin,stncode[origin],TrainDate)
        df2=df2[df2['Cost']<=mxval[1]]
        logging.warning('t1 over')
        l1=[]
        for i in range(len(df1)):
            l1.append(df1.iloc[i].values)

        logging.warning('l1 over')
        l2=[]
        for i in range(len(df2)):
            l2.append(df2.iloc[i].values)
        logging.warning('l2 over')
        
        return render(request,'app1/display.html',{'f':False,'t':False,'ft':True,'df1':df1,'df2':df2,'values1':l1,'values2':l2,'empty1':len(df1)==0,'empty2':len(df2)==0})

    return render(request,'app1/display.html',{'transport':0})