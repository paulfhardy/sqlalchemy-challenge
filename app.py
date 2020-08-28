#################################################
# CREATED BY PAUL HARDY
# CREATED ON 08-27-2020
#################################################
from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################
# Database Setup - connect to hawaii.sqllite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the hawaii.sqllite database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each of the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Home page with available routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the SQL Alchemy Hawaii weather page!<br/>"
        f"_______________________________________________<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Weather Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature Observations</a><br/>"
        f"<a href='/api/v1.0/2016-01-01'>Temperature Summary stats from January 1 2016 onwards.</a><br/>"
        f"<a href='/api/v1.0/2016-05-01/2016-05-15'>Temperature Summary stats between May 1st 2016 and May 15th 2016</a><br/>"          
           )

# Additional static routes        
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data for the last year including the date and prcp measurements"""
    
    #prcp_measurements = session.query(Measurement.date, Measurement.prcp).all()
    
    prcp_measurements = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date > '2016-08-23').\
                        order_by(Measurement.date).all()
    
    # Close session to the DB
    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in prcp_measurements:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.station).all()

    # Close session to the DB
    session.close()
    
    #print(results)
    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs data for the most recent year including the date and tobs measurement"""
    
    temp_hist = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station=="USC00519281").\
        filter(Measurement.date >= '2016-08-18').\
        filter(Measurement.date <= '2017-08-18').all()
    
    # Close session to the DB
    session.close()
    #print(temp_hist)
    
    # Create a dictionary from the row data and append to a list of all_temp_hist
    all_temp_hist = []
    for date, tobs in temp_hist:
        temp_hist_dict = {}
        temp_hist_dict["date"] = date
        temp_hist_dict["tobs"] = tobs
        all_temp_hist.append(temp_hist_dict)

    return jsonify(all_temp_hist)

@app.route("/api/v1.0/<start>")
def temp_summary_stats(start):
    """Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start date"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp_summary = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    print(temp_summary)
    
    # Close session to the DB
    session.close()
    
    temp_summ_list = []
    for item in temp_summary:
        item_dict = {}
        item_dict["TMIN"] = item[0]
        item_dict["TMAX"] = item[1]
        item_dict["TAVG"] = item[2]
        temp_summ_list.append(item_dict)

    return jsonify(temp_summ_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_range_summary_stats(start,end):
    """Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start date and end date range"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp_range_summary = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        filter(Measurement.date >= end).all()
       
    # Close session to the DB
    session.close()
    
    temp_range_summ_list = []
    for item in temp_range_summary:
        item_dict = {}
        item_dict["TMIN"] = item[0]
        item_dict["TMAX"] = item[1]
        item_dict["TAVG"] = item[2]
        temp_range_summ_list.append(item_dict)

    return jsonify(temp_range_summ_list)

if __name__ == "__main__":
    app.run(debug=True)