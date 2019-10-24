import os
import csv

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
sf_salaries = Base.classes.SF_salary_data_gender
sf_salaries_year = Base.classes.SF_gender_data_gender_year

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index3.html")


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(sf_salaries).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    id_list = df["Id"].tolist()
    # Return a list of the column names (sample names)
    
    return jsonify(id_list)

@app.route("/year")
def years():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(sf_salaries_year).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    year_list = df["Year"].tolist()
    # Return a list of the column names (sample names)
    
    return jsonify(year_list)

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
            sf_salaries.JobTitle,
            sf_salaries.gender
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
        salary_dict["Gender"] = result[9]
        
    return jsonify(salary_dict)

@app.route("/year/<Year>")
def salaries_year (Year):
    """Return the MetaData for a given sample."""
    sel4 = [
            sf_salaries_year.Year,
            sf_salaries_year.BasePay,
            sf_salaries_year.OvertimePay,
            sf_salaries_year.OtherPay,
            sf_salaries_year.Benefits,
            sf_salaries_year.TotalPay,
            sf_salaries_year.TotalPayBenefits
        ]

    results = db.session.query(*sel4).filter(sf_salaries_year.Year == Year).all()
    
    salary_dict_year = {}
    for result in results:
        salary_dict_year["Year"] = result[0]
        salary_dict_year["BasePay"] = result[1]
        salary_dict_year["OvertimePay"] = result[2]
        salary_dict_year["OtherPay"] = result[3]
        salary_dict_year["Benefits"] = result[4]
        salary_dict_year["TotalPay"] = result[5]
        salary_dict_year["TotalPayBenefits"] = result[6]
    return jsonify(salary_dict_year)


@app.route("/index2.html")
def index2():
    return render_template('index2.html')

@app.route("/index4.html")
def index4():
    return render_template('index4.html')

@app.route("/index5.html")
def index5():
    return render_template('index5.html')

@app.route("/index.html")
def d3():
    return render_template('index.html')

@app.route("/assets/data/SF_salary_data_gender.csv")
def scatter():

    sel3 = [
            sf_salaries.Id,
            sf_salaries.TotalPay,
            sf_salaries.OvertimePay,
            sf_salaries.Benefits,
            sf_salaries.TotalPayBenefits,
            sf_salaries.Year,
            sf_salaries.JobTitle,
            sf_salaries.gender
        ]

    results = db.session.query(*sel3).all()
    
    salary_list2 = []
    for result in results:
        salary_dict2 = {}
        salary_dict2["Id"] = result[0]
        salary_dict2["TotalPay"] = result[1]
        salary_dict2["OvertimePay"] = result[2]
        salary_dict2["Benefits"] = result[3]
        salary_dict2["TotalPayBenefits"] = result[4]
        salary_dict2["Year"] = result[5]
        salary_dict2["JobTitle"] = result[6]
        salary_dict2["Gender"] = result[7]
        salary_list2.append(salary_dict2)
    #data = pd.read_csv("DataSets/SalariesClean.csv")

    #df = pd.DataFrame(data)

    return jsonify(salary_list2)

if __name__ == "__main__":
    app.run()