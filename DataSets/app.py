import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/database.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
sf_salaries = Base.classes.Salaries

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/data/<Id>")
def sample_values(Id):
    
    stmt = db.session.query(sf_salaries).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    
    #session = Session(engine)
    #results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()
    #print(df)

    # Create a dictionary from the row data and append to a list of all_passengers
    
    sample_data = df.loc[df['Id'] >= 0]

    salaries_dict = {
        "Id": sample_data.Id.values.tolist(),
        "EmployeeName": sample_data.EmployeeName.values.tolist(),
        "JobTitle": sample_data.JobTitle.values.tolist(),
        "BasePay": sample_data.BasePay.values.tolist(),
        "OvertimePay": sample_data.OvertimePay.values.tolist(),
        "OtherPay": sample_data.OtherPay.values.tolist(),
        "Benefits": sample_data.Benefits.values.tolist(),
        "TotalPay": sample_data.TotalPay.values.tolist(),
        "TotalPayBenefits":sample_data.TotalPayBenefits.values.tolist(),
        "Year":sample_data.Year.values.tolist(),
        "Notes":sample_data.Notes.values.tolist(),
        "Agency": sample_data.Agency.values.tolist(),
        "Status": sample_data.Status.values.tolist()
    }
        

    return jsonify(salaries_dict)



if __name__ == '__main__':
    app.run()
