from pathlib import Path
from flask import Flask, render_template, make_response, send_from_directory, request
from flask_cors import CORS

import logging

# Sets up the Flask application
app = Flask(__name__, template_folder='templates')
app.secret_key = 'Secret Key 123'
tasks_data = {}
CORS(app)



@app.route("/", methods=["GET"])
def return_home():
    return render_template('index.html')

@app.route("/form/", methods = ["GET"])
def return_form():
    return render_template('predict.html')

@app.route("/about/", methods = ["GET"])
def return_about():
    return render_template('about.html')

@app.route("/service/", methods = ["GET"])
def return_service():
    return render_template('service.html')


@app.route("/results/", methods = ["GET"])
def return_results():
    return render_template('results.html')


@app.route('/form/', methods = ["POST"])
def get_form():
    income = int(request.form.get('income'))
    investments = int(request.form.get('investments'))
    retirementAge = int(request.form.get('retirementAge'))
    currentAge = int(request.form.get('currentAge'))
    lifestyle = request.form.get('lifestyle')


    #Come up with some kind of algo to give suggestions
    #Suggestions can be stock suggestions, investment opportunities, etc
    #Breakdown of more volatile and less volatile stocks. 


    net_worth = income + investments
    increments = net_worth // 20

    volatile_stocks_interest = 0.06
    negative_volatile_stocks_interest = -0.1
    medium_stocks_interest = 0.03
    negative_medium_stocks_interest = -0.04
    low_risk_stocks_interest = 0.01

    if lifestyle == "Budget":
        lifestyle_amount = 2000
    elif lifestyle == "Standard":
        lifestyle_amount = 3000
    else:
        lifestyle_amount = 4000


    lifeExpectancy = 75
    
    delta_age = lifeExpectancy - retirementAge
    

    net_worth = income + investments
    increments = net_worth // 20

    volatile_stocks_interest = 0.06
    negative_volatile_stocks_interest = -0.1
    medium_stocks_interest = 0.03
    negative_medium_stocks_interest = -0.04
    low_risk_stocks_interest = 0.01

    if lifestyle == "Budget":
        lifestyle_amount = 2000
    elif lifestyle == "Standard":
        lifestyle_amount = 3000
    else:
        lifestyle_amount = 4000

    random_other_expenses = 50000
    delta = retirementAge - currentAge
    required_amount_of_money = delta_age * lifestyle_amount * 12 + random_other_expenses
    print(required_amount_of_money)



    min_volatility = 8431804810948109841
    best_outcome = (0,0,0)
    best_return = 0
    for i in range(0, 20):
        for j in range(0,20):
            #We want i*increments invested into volatile, j * increments into medium, 20-i-j * increments into low
            max_return_investing_on_volatile_stocks = compute_amount(volatile_stocks_interest, i * increments, delta)
            min_return_investing_on_volatile_stocks = compute_amount(negative_volatile_stocks_interest, i * increments, delta)
            max_return_investing_on_medium_stocks = compute_amount(medium_stocks_interest, j*increments , delta)
            min_return_investing_on_medium_stocks = compute_amount(negative_medium_stocks_interest, j*increments, delta)
            return_investing_on_low_stocks = compute_amount(low_risk_stocks_interest, (20-i-j)*increments, delta)

            total_return = max_return_investing_on_volatile_stocks + max_return_investing_on_medium_stocks + return_investing_on_low_stocks 
            
            volatility_volatile = max_return_investing_on_volatile_stocks - min_return_investing_on_volatile_stocks
            volatility_medium = max_return_investing_on_medium_stocks - min_return_investing_on_medium_stocks

            total_volatility = volatility_volatile + volatility_medium
            if total_volatility < min_volatility and total_return >= required_amount_of_money:
                print(total_return)
                min_volatility = total_volatility
                best_outcome = (i,j,20-i-j)
                best_return = total_return
    print(best_outcome)

    best_return = int(best_return)


    max_outcome = compute_amount(volatile_stocks_interest, net_worth, delta)
    min_outcome = compute_amount(negative_volatile_stocks_interest, net_worth, delta)
    volatility_outcomes_max = max_outcome - min_outcome
    percentage_risk_max = min(100, volatility_outcomes_max / net_worth * 50)

    max_medium_outcome = compute_amount(medium_stocks_interest, net_worth, delta)
    min_medium_outcome = compute_amount(negative_medium_stocks_interest, net_worth, delta)
    volatility_outcomes_medium = max_medium_outcome - min_medium_outcome
    percentage_risk_medium = min(100, volatility_outcomes_medium / net_worth * 50)
    
    max_low_outcome = compute_amount(low_risk_stocks_interest, net_worth, delta)
    
    volatility_outcomes_low = 0 
    percentage_risk_low = 0

    percentage_risk = min(100, min_volatility / net_worth * 50)
    data = {best_outcome: round(percentage_risk, 2)}
    risky = {int(max_outcome): round(percentage_risk_max,2)}
    medium = {int(max_medium_outcome): round(percentage_risk_medium,2)}
    low = {int(max_low_outcome): round(percentage_risk_low,2)}
    money = required_amount_of_money



   

    #Do something with it, and render our results template and give it the values we compute. Also update the dashboard [when needbe]
    return render_template('results.html', data = data, increments = increments, risky = risky, medium = medium, low = low, money = money, best_return = best_return)

def compute_amount(interest_rate, principal, delta):
    
    return principal * (1 + interest_rate) ** delta


if __name__ == '__main__':
   app.run()