# some comment here
from .a_model import modelIt
from flaskexample import app
from flask import render_template, request, send_from_directory

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html");

@app.route('/result', methods=['POST'])
def result():
    user_input = []
    for feature in ['q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20']:
        if request.form.get(feature): user_input.append(1)
        else: user_input.append(0)
    #user_input = [ int(request.form.get(feature))
    #               for feature in  ['q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20'] ]
    print(user_input)
    label = modelIt(user_input)
    return render_template("result.html", user_input = user_input, label = label)
