from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template,url_for, redirect,request
from flask_sqlalchemy import SQLAlchemy

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

date_range = pd.date_range(start='1/1/2010', end='1/1/2011')



@app.route("/")
def index(): 
    """Return the homepage."""
    return render_template("index.html")



@app.route("/api/v1.0/precipitation")
def precipitation():
        # Design a query to retrieve the last 12 months of precipitation data and plot the results
    date_range = pd.date_range(start='1/1/2010', end='1/1/2011')
    date_range_array = date_range.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    date_ray = []
    prcp_array = []
    # Calculate the date 1 year ago from the last data point in the database

    # Perform a query to retrieve the data and precipitation scores
    for x in list(range(0,len(date_range_array))):
        date_ray.append( date_range_array[x])
        prcp_array.append( engine.execute('select prcp from Measurement where date = "'+date_range_array[x]+'"').fetchall())

    prcp_mean_list = []
    for a in list(range(0,len(date_range_array))):
        ct = 0
        ct2 = 0
        for b in list(range(0,len(prcp_array[a]))):
            try:
                ct = ct + prcp_array[a][b][0]
            except:
                ct2 = ct2 + 1
        try:    
            prcp_mean_list.append(ct/(len(prcp_array[a])-ct2))
        except:
            
            prcp_mean_list.append(0)
    
    empty_dictionary = {}
    for x in list(range(0,len(prcp_mean_list))):
        empty_dictionary.update( {date_range_array[x] : prcp_mean_list[x]} )


    return jsonify(empty_dictionary)


@app.route("/api/v1.0/stations")
def stations():
    temp_dict = {}
    for x in list(range(0,len(engine.execute("select station from station").fetchall()))):
        temp_dict.update({engine.execute("select station from station").fetchall()[x][0]:engine.execute("select station from station").fetchall()[x][0]})
    
    return jsonify(temp_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    date_range = pd.date_range(start='1/1/2010', end='1/1/2011')
    date_range_array = date_range.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    for_dict = []
    date_ray = []
    temp_array = []
    # Calculate the date 1 year ago from the last data point in the database

    # Perform a query to retrieve the data and precipitation scores
    for x in list(range(0,len(date_range_array))):
        for_dict.append( engine.execute('select date, prcp from Measurement where date = "'+date_range_array[x]+'"').fetchall())
        date_ray.append( date_range_array[x])
        temp_array.append(engine.execute('select tobs from Measurement where date = "'+date_range_array[x]+'"').fetchall())
    # Save the query results as a Pandas DataFrame and set the index to the date column
    temp_mean_list = []

    for a in list(range(0,len(date_range_array))):
        ct = 0
        ct2 = 0
        for b in list(range(0,len(temp_array[a]))):
            try:
                ct = ct + temp_array[a][b][0]
            except:
                ct2 = ct2 + 1
        try:    
            temp_mean_list.append(ct/(len(temp_array[a])-ct2))
        except:
            temp_mean_list.append("null")
    
    temp_dict = {}
    for x in list(range(0,len(temp_mean_list))):
        temp_dict.update({date_ray[x]:temp_mean_list[x]})
    
    return jsonify(temp_dict)



@app.route("/api/v1.0/<month>/<day>/<year>")
def start(month,day,year):
    date_range = pd.date_range(start=month+"/"+day+"/"+year, end='08/23/2017')
    date_range_array = date_range.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    for_dict = []
    date_ray =[]
    temp_array = []
    for x in list(range(0,len(date_range_array))):
        date_ray.append( date_range_array[x])
        temp_array.append(engine.execute('select tobs from Measurement where date = "'+date_range_array[x]+'"').fetchall())

    temp_mean_list = []

    for a in list(range(0,len(date_range_array))):
        ct = 0
        ct2 = 0
        for b in list(range(0,len(temp_array[a]))):
            try:
                ct = ct + temp_array[a][b][0]
            except:
                ct2 = ct2 + 1
        try:    
            temp_mean_list.append(ct/(len(temp_array[a])-ct2))
        except:
            temp_mean_list.append("null")
    a=sum(temp_mean_list)/len(temp_mean_list)
    data = {
        "Tmin":min(temp_mean_list),
        "Tmax":max(temp_mean_list),
        "Tavg":a
    }
    return jsonify(data)


@app.route("/api/v1.0/<month1>/<day1>/<year1>/<month2>/<day2>/<year2>")
def start1(month1,day1,year1,month2,day2,year2):
    date_range = pd.date_range(start=month1+"/"+day1+"/"+year1, end=month2+"/"+day2+"/"+year2)
    date_range_array = date_range.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    for_dict = []
    date_ray =[]
    temp_array = []
    for x in list(range(0,len(date_range_array))):
        date_ray.append( date_range_array[x])
        temp_array.append(engine.execute('select tobs from Measurement where date = "'+date_range_array[x]+'"').fetchall())

    temp_mean_list = []

    for a in list(range(0,len(date_range_array))):
        ct = 0
        ct2 = 0
        for b in list(range(0,len(temp_array[a]))):
            try:
                ct = ct + temp_array[a][b][0]
            except:
                ct2 = ct2 + 1
        try:    
            temp_mean_list.append(ct/(len(temp_array[a])-ct2))
        except:
            temp_mean_list.append("null")
    a=sum(temp_mean_list)/len(temp_mean_list)
    data = {
        "Tmin":min(temp_mean_list),
        "Tmax":max(temp_mean_list),
        "Tavg":a
    }
    return jsonify(data)




if __name__ == "__main__":
    app.run()
