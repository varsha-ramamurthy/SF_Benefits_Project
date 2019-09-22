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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/databaseclean.sqlite"
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


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(sf_salaries).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    id_list = df["Id"].tolist()
    # Return a list of the column names (sample names)
    
    return jsonify(id_list)


@app.route("/data/<Id>")
def salaries_id (Id):
    """Return the MetaData for a given sample."""
    sel2 = [
            sf_salaries.Id,
            sf_salaries.EmployeeName,
            sf_salaries.BasePay,
            sf_salaries.OvertimePay,
            sf_salaries.OtherPay,
            sf_salaries.Benefits,
            sf_salaries.TotalPayBenefits,
            sf_salaries.Year,
            sf_salaries.JobTitle
        ]

    results = db.session.query(*sel2).filter(sf_salaries.Id == Id).all()
    
    salary_dict = {}
    for result in results:
        salary_dict["Id"] = result[0]
        salary_dict["EmployeeName"] = result[1]
        salary_dict["BasePay"] = result[2]
        salary_dict["OvertimePay"] = result[3]
        salary_dict["OtherPay"] = result[4]
        salary_dict["Benefits"] = result[5]
        salary_dict["TotalPayBenefits"] = result[6]
        salary_dict["Year"] = result[7]
        salary_dict["JobTitle"] = result[8]
        
    return jsonify(salary_dict)

@app.route("/samples/<Id>")
def samples(Id):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(sf_salaries).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df['Id'] > 0, ["Year", "TotalPayBenefits", Id]]
    # Format the data to send as json
    data = {
        "Year": sample_data.Year.values.tolist(),
        "Id": sample_data[Id].values.tolist(),
        "TotalPayBenefits": sample_data.TotalPayBenefits.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()