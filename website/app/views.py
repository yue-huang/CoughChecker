# some comment here
from .a_model import modelIt
from app import app
from flask import render_template, request, send_from_directory

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html");

@app.route('/result', methods=['POST'])
def result():
    user_input = []

    if request.form.get('q1'):
        user_input.append(int(request.form.get('q1')))
    else:
        user_input.append(92/2)

    if request.form.get('q2'):
        user_input.append(int(request.form.get('q2')))
    else:
        user_input.append((77-19)/2)

    if request.form.get('q3'):
        user_input.append(1)
    else:
        user_input.append(0)

    if request.form.get('q4'):
        symptom_type = int(request.form.get('q4'))
        if symptom_type == 1:
            user_input = user_input + [1,0,0]
        elif symptom_type == 2:
            user_input = user_input + [0,1,0]
        elif symptom_type == 3:
            user_input = user_input + [0,0,1]
        else:
            user_input = user_input + [0,0,0]
    else:
        user_input = user_input + [0,0,0]

    for feature in ['q7','q8','q9','q10','q11','q12','q13','q14','q15']:
        if request.form.get(feature):
            user_input.append(1)
        else:
            user_input.append(0)

    #user_input = [ int(request.form.get(feature))
    #               for feature in  ['q1','q2','q3']
    #               ]
    print(user_input)
    label = modelIt(user_input)
    return render_template("result.html", user_input = user_input, label = label)
