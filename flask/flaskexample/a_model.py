# some comments

def modelIt(user_input, model_file_name = 'flaskexample/data/finalized_model.sav'):
    import pickle
    import numpy as np
    est_loaded = pickle.load(open(model_file_name, 'rb'))
    testprob = est_loaded.predict_proba(np.array([user_input])).item((0,1))
    #print('the test prob is:', testprob)
    return "{0:.0f}%".format(testprob*100)
#modelIt([1,1,1,1,1])
