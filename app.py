from pathlib import Path
from flask import Flask, render_template, make_response, send_from_directory, request, session
from flask_cors import CORS
import pyrebase
import logging
import json
import os

# Sets up the Flask application
app = Flask(__name__, template_folder='templates')
app.secret_key = 'Secret Key 123'
apiKey = os.environ.get("apiKey")
appId = os.environ.get("appId")
databaseURL = os.environ.get("databaseURL")
measurementId = os.environ.get("measurementId")
messagingSenderId = os.environ.get("messagingSenderId")
projectId = os.environ.get("projectId")
storageBucket = os.environ.get("storageBucket")
authDomain = os.environ.get("authDomain")

config = {'apiKey':apiKey, 'appId': appId, 'databaseURL':databaseURL, "measurementId":measurementId, "projectId":projectId, "storageBucket" : storageBucket, "authDomain" : authDomain}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()



CORS(app)



@app.route("/", methods=["GET"])
def return_home():
    return render_template('index.html', authed = 'user' in session)

@app.route("/form/", methods = ["GET"])
def return_form():
    return render_template('predict.html', authed = 'user' in session)

@app.route("/logout/", methods = ["GET"])
def logout():
    session.pop('user', None)
    return render_template('index.html', authed = False)# should be false)

@app.route("/about/", methods = ["GET"])
def return_about():
    return render_template('about.html', authed = 'user' in session)

@app.route("/dashboard/", methods = ["GET"])

def return_dashboard():
    print(session['user'])    
    if 'user' not in session:
        return render_template('index.html', authed = False)
    
    details = db.child(session['user']['localId']).get()
    if details.val() == None:
        return render_template('dashboard.html', user = session['user'], details = None, not_predicted = True)
    print(details.val())
    details = dict(details.val())
    optimal_dict = details['optimal']
    current_key = next(iter(optimal_dict))  # Get the single key in 'optimal' dict

# Convert the string key to a tuple
    new_key = tuple(map(int, current_key.split('_')))

# Replace the key in the 'optimal' dictionary
    details['optimal'] = {new_key: optimal_dict[current_key]}
    print(details)
   

    return render_template('dashboard.html', user= session['user'], details = details, not_predicted = False)


@app.route("/results/", methods = ["GET"])
def return_results():
    return render_template('results.html')

@app.route("/login/", methods = ['GET','POST'])
def login():
    if 'user' in session:
        return render_template('index.html', authed = True)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            details = db.child(session['user']['localId']).get()
            if details.val() == None:
                return render_template('dashboard.html', user = session['user'], details = None, not_predicted = True)
            print(details.val())
            details = dict(details.val())
            optimal_dict = details['optimal']
            current_key = next(iter(optimal_dict))  # Get the single key in 'optimal' dict

        # Convert the string key to a tuple
            new_key = tuple(map(int, current_key.split('_')))

        # Replace the key in the 'optimal' dictionary
            details['optimal'] = {new_key: optimal_dict[current_key]}
            return render_template('dashboard.html', user= session['user'], details = details, not_predicted = False)
        except:
            return "Failed to login"
    return render_template('login.html', authed = 'user' in session)


@app.route("/register/", methods = ['GET','POST'])
def register():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        if password != confirm_password:
            return "Failed to register: Password and confirmation are different."

        try:
            print(email,password)
            user = auth.create_user_with_email_and_password(email, password)
            print("Hello!")
            session['user'] = user
            print("Here")
            return render_template('dashboard.html', not_predicted = True, details = None)
        
        except Exception as e:
            print(e)
            return "Failed to Register"
    return render_template('register.html', authed = 'user' in session)

                                                                                                                                                                                                                                                                                                                                                             

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


    lifeExpectancy = 90
    
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


    concat_data = '_'.join(map(str, best_outcome))
    data_db = {concat_data: round(percentage_risk, 2)}
    user = session['user']

    db.child(user['localId']).set({'optimal': data_db, 'increments': increments, 'risky': risky, 'medium': medium, 'low': low, "money" : money, "best_return" : best_return})


    

    #Do something with it, and render our results template and give it the values we compute. Also update the dashboard [when needbe]
    return render_template('results.html', data = data, increments = increments, risky = risky, medium = medium, low = low, money = money, best_return = best_return, authed = 'user' in session)

def compute_amount(interest_rate, principal, delta):
    
    return principal * (1 + interest_rate) ** delta


if __name__ == '__main__':
   app.run()