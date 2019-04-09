import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import pandas as pd
import datetime as dt
from datetime import timedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to both tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to My Hawaii Climate App!<br/>"
        f"Here are Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return one year precipitation data"""
    # bringing start & end dates:
    EndDate = dt.date(2017, 8, 23)
    OneYear = timedelta(days=365)
    StartDate = EndDate - OneYear
    
    # Query precipitation data for last year
    P_Results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date>=StartDate).filter(Measurement.date<=EndDate).all()

    # Return JSON representation of precipitation data dictionary
    precipitation_dict = list(np.ravel(P_Results))
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    S_Results = session.query(Station.station).all()

    # Return JSON representation of stations data dictionary
    stations_dict = list(np.ravel(S_Results))
    return jsonify(stations_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return one year precipitation data"""
    # bringing start & end dates:
    EndDate = dt.date(2017, 8, 23)
    OneYear = timedelta(days=365)
    StartDate = EndDate - OneYear

    # Query the primary station for all tobs from the last year
    temp_data = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date>=StartDate).filter(Measurement.date<=EndDate).all()

    # Return JSON representation of stations data dictionary
    temp_data_dict = list(np.ravel(temp_data))
    return jsonify(temp_data_dict)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return tmin, tavg, tmax data"""
    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        temp_data = session.query(*sel).\
        filter(Measurement.date >= start).all()
         # Return JSON representation of temp data dictionary
        temp_data_dict = list(np.ravel(temp_data))
        return jsonify(temp_data_dict)

    temp_data = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
         # Return JSON representation of temp data dictionary
    temp_data_dict = list(np.ravel(temp_data))
    return jsonify(temp_data_dict)


if __name__ == '__main__':
    app.run(debug=True)
