import pickle

def save_data_pickle(data,filename='default'):
    pklfile = open(filename,'wb')
    pickle.dump(data,pklfile)
    pklfile.close()

def load_data_pickle(filename):
    pklfile = open(filename,'rb')
    data = pickle.load(pklfile)
    pklfile.close()
    return data