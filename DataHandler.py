
import numpy as np
import numba
import sklearn as sk
import copy
from sklearn.preprocessing import normalize

'''

Creates a data manipulator class to sample, recombine and resample data

'''
class DataHandler:
    def __init__(self, path, token=',', scaled=False):
        self.token = token
        self.path = path
        self.all_data = self.load_data(path)
        self.num_features = len(self.all_data.T)-1
        self.num_samples = len(self.all_data)


    @numba.jit
    def load_data(self, path):
        if(self.token is not None):
            return np.loadtxt(path, delimiter=self.token)  # read file into array
        else:
            return np.loadtxt(path)  # read file into array

    def scale(self, option=None, num_labels=None):
        if(option==0) or (option==None):
            self.all_data = sk.preprocessing.maxabs_scale(self.all_data) # scale the data to [-1, 1]
            return self.cleave(self.all_data)
        elif(option==1):
            x, y = self.cleave()
            y = sk.preprocessing.LabelEncoder(y, num_labels)
            y = sk.preprocessing.OneHotEncoder(y, num_labels)


    """
    The cleave() method separates data into an input vector and a target
    for regression and classification
    """
    def cleave(self):
        x = copy.copy(self.all_data[:,0:-1])
        y = copy.copy(self.all_data[:,-1:])
        return x, y

    """
    The reload() method loads a new set of data into the DataHandler object
    """
    def reload(self, path=None, token=None):
        if(path is not None):
            self.path = path
        self.token = token
        self.all_data = self.load_data(self.path)
