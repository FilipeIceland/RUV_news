'''
create, read, update pkl files
'''
import pickle

def create_pkl(filename, dictt = {}):
    f = open(filename , 'wb')
    pickle.dump(dictt , f)
    f.close()
    
def read_pkl(filename): 
    f = open(filename, 'rb')
    pkl = pickle.load(f)     
    f.close()
    return pkl['data_frame']

def update_pkl(df, filename): 
    f = open(filename , 'wb')
    pickle.dump({"data_frame": df}, f)
    f.close()
