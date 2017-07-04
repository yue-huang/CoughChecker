# Predict health condition, the need to see a doctor, and the mostly likely cause for users,
# based on user's input information using a pre-trained logistic regression predictive model.


def modelIt(user_input, model_file_name='app/data/finalized_model.sav'):
    import pickle
    import numpy as np

    # Convert age to the same scale as in the model
    user_input[0] = user_input[0] / 92
    #print('Edited user input:', user_input)

    # Load the model and predict
    est_loaded = pickle.load(open(model_file_name, 'rb'))
    testprob = est_loaded.predict_proba(np.array([user_input])).item((0, 1))
    y_predict = est_loaded.predict(np.array([user_input]))[0]
    #print('the test prob and predicted class are:', testprob, y_predict)

    # Generate output information
    if y_predict == 1:
        label = [
            'Caution! ',
            'severe',
            ' Please visit your healthcare provider soon!',
            'asthma',
            'severe_condition.png'
        ]
    if y_predict == 0:
        label = [
            'Good news!',
            'mild',
            ' Feel free to recover by yourself. Please keep monitoring your symptoms.',
            'upper respiratory infection',
            'mild_condition.png'
        ]
    return label
