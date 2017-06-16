# some comments

def modelIt(user_input, model_file_name = 'flaskexample/data/finalized_model.sav'):
    import pickle
    import numpy as np
    est_loaded = pickle.load(open(model_file_name, 'rb'))
    testprob = est_loaded.predict_proba(np.array([user_input])).item((0,1))
    y_predict = est_loaded.predict(np.array([user_input]))[0]
    if y_predict == 1: label = ['sorry that you may have a severe condition. Please visit your healthcare provider soon!','severe_condition.png']
    if y_predict == 0: label = ['congratulations! You have a mild condition. Feel free to recover by yourself. Please keep monitoring your symptoms.','mild_condition.png']
    print('the test prob and predicted class are:', testprob, y_predict)
    #return "{0:.0f}%".format(testprob*100)
    return label
#modelIt([1,1,1,1,1])
