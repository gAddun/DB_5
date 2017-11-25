
import numpy as np
import numba
import sklearn as sk
from sklearn.preprocessing import normalize

'''

Creates a data manipulator class to sample, recombine and resample data

'''
class DataHandler:
    def __init__(self, path, folds, token=None, scaled=False):
        self.token = token
        #scale numeric data to [-1, 1]
        if(scaled==True):
            self.all_data = sk.preprocessing.maxabs_scale(self.load_data(path))#scale the data to [-1, 1]
        else:
            self.all_data = self.load_data(path)
        self.num_features = len(self.all_data.T)-1


    @numba.jit
    def load_data(self, path):
        if(self.token is not None):
            return np.loadtxt(path, delimiter=self.token)  # read file into array
        else:
            return np.loadtxt(path)  # read file into array


    """
    The cleave() method separates data into an input vector and a target
    for regression and classification
    """
    def cleave(self, in_matrix):
        x = in_matrix[:,0:-1]
        y = in_matrix[:,-1:]
        return x, y

    """
    The reload() method loads a new set of data into the DataHandler object
    """
    def reload(self, path, token=None):
        self.token = token
        self.all_data = self.load_data(path)

    def recombine(self, num_folds):
        temp_array = self.folds_container[0]
        for i in range(0, self.num_folds-1):
            temp_array = np.vstack((temp_array, self.folds_container[i+1]))
        np.random.shuffle(temp_array)
        self.folds_container.clear()
        self.fold(temp_array, num_folds)