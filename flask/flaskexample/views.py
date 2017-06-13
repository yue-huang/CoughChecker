# some comment here
from .a_model import modelIt
from flaskexample import app
from flask import render_template, request

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html");

@app.route('/result', methods=['POST'])
def result():
    user_input = [ int(request.form.get(feature))
                   for feature in  ['q1','q2','q3','q4','q5'] ]
    print(user_input)
    prob = modelIt(user_input)
    return render_template("result.html", user_input = user_input, prob = prob)
