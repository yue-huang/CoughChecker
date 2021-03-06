# Set up index and result html pages
# Accept user input, predict health condition, and return the results

from .a_model import modelIt
from app import app
from flask import render_template, request, send_from_directory


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route('/result', methods=['POST'])
def result():
    '''
    Parse user input, predict, and return the result page.
    '''
    user_input = []

    if request.form.get('q1'):
        user_input.append(int(request.form.get('q1')))
    else:
        user_input.append(92 / 2)

    if request.form.get('q2'):
        user_input.append(1)
    else:
        user_input.append(0)

    if request.form.get('q3'):
        symptom_type = int(request.form.get('q3'))
        if symptom_type == 1:
            user_input = user_input + [1, 0]
        elif symptom_type == 2:
            user_input = user_input + [0, 1]
        else:
            user_input = user_input + [0, 0]
    else:
        user_input = user_input + [0, 0]

    for feature in ['q4', 'q5', 'q6', 'q7', 'q8', 'q9']:
        if request.form.get(feature):
            user_input.append(1)
        else:
            user_input.append(0)

    # user_input = [ int(request.form.get(feature))
    #               for feature in  ['q1','q2','q3']
    #               ]

    print(user_input)
    label = modelIt(user_input)
    return render_template("result.html", label=label)
