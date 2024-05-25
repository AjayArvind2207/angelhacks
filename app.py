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

@app.route('/form/', methods = ["POST"])
def get_form():
    income = request.form.get('income')
    investments = request.form.get('investments')
    retirementAge = request.form.get('retirementAge')
    currentAge = request.form.get('currentAge')
    lifestyle = request.form.get('lifestyle')
    
    print(income, investments, retirementAge, currentAge, lifestyle)

    #Do something with it, and render our results template and give it the values we compute. Also update the dashboard [when needbe]
    return render_template('index.html')


if __name__ == '__main__':
   app.run()