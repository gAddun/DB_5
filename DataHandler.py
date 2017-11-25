
import numpy as np
import numba
import sklearn as sk
import copy
from sklearn import preprocessing as pre
from sklearn.preprocessing import normalize

'''

Creates a data manipulator class to sample, recombine and resample data

'''
class DataHandler:
    def __init__(self, path, token=','):
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


    """
    The scale() function returns scaled data
    The function takes optional arguments where
        + option determines the type of scaling applied to the data
        + num_labels is the number of labels or classes for classification problems
    """
    def scale(self, option=None, num_labels=None, labels=None):
        #if no option selected, just separate targets from inputs
        if(option == None):
            return self.cleave()
        # scale data to [-1, 1]
        elif(option==0):
            self.all_data = sk.preprocessing.maxabs_scale(self.all_data) # scale the data to [-1, 1]
            return self.cleave()
        #Multi-Label, categorical encoding for SVM
        elif(option==1):
            x, y = self.cleave()
            #preprocess y into binary labeled encoded matrix
            lb = pre.LabelBinarizer()
            y = lb.fit_transform(y)
            y = pre.OneHotEncoder(y, num_labels)
            #scale x values
            x = pre.maxabs_scale(x)
            return x, y


    """
    The cleave() method separates data into an input vector and a target
    for regression and classification
    """
    def cleave(self):
            x = copy.copy(self.all_data[:,0:-1])
            y = copy.copy(self.all_data[:,-1:])
            return x, y


    """
    The fold() function creates two containers, fold_x[] and fold_y[]
    These containers hold num_folds # of arrays of samples from the data
    The input vector arrays in fold_x[i] correspond to the target vectors in fold_y[i]
    """
    def fold(self, num_folds):
        x_folds = []
        y_folds = []
        #Sets bin as the number of samples per array
        if (self.num_samples % num_folds == 0):
            bin = (self.num_samples / num_folds)
        else:
            bin = (self.num_samples // num_folds)
        #For the first n-1 folds, use bin as start and stop index
        for i in range(0, num_folds-1):
            x = copy.copy(self.all_data[(i*bin):(i*(bin+1)), 0:-1])
            y = copy.copy(self.all_data[(i*bin):(i*(bin+1)), -1:])
            #add the folded data to the folds containers
            x_folds.append(x)
            y_folds.append(y)
        #for the last fold, do not use index stopping value
        x = copy.copy(self.all_data[(i * bin):, 0:-1])
        y = copy.copy(self.all_data[(i * bin):, -1:])
        # add the folded data to the folds containers
        x_folds.append(x)
        y_folds.append(y)
        return x_folds, y_folds


    """
    The reload() method loads a new set of data into the DataHandler object
    """
    def reload(self, path=None, token=None):
        self.path = path
        self.token = token
        self.all_data = self.load_data(self.path)
