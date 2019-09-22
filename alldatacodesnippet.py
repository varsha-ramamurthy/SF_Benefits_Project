@app.route("/data")
def salaries ():
    """Return the MetaData for a given sample."""
    sel3 = [
            sf_salaries.Id,
            sf_salaries.TotalPayBenefits,
            sf_salaries.Year, 
            sf_salaries.JobTitle
        ]

    #results = db.session.query(*sel).filter(sf_salaries.Id == Id).all()
    results = db.session.query(*sel3).all()
#sf_salaries.Id,sf_salaries.EmployeeName, sf_salaries.JobTitle
    #Create a dictionary entry for each row of information
    #salary_data = {}
    salary_data = []
    for result in results:
        salary_dict2 = {}
        salary_dict2["Id"] = result[0]
        salary_dict2["TotalPayBenefits"] = result[1]
        salary_dict2["Year"] = result[2]
        salary_dict2["JobTitle"] = result[3]
        salary_data.append(salary_dict2)
        
    print(salary_data)
    return jsonify(salary_data)