
import numpy as np
import numba
import sklearn as sk
import copy
from sklearn import preprocessing as pre
import pandas as pd
from sklearn.preprocessing import normalize

'''

Creates a data manipulator class to sample, recombine and resample data

'''
class DataHandler:
    def __init__(self, path, token=None, all_numeric=True):
        self.token = token
        self.path = path
        self.all_data = self.load_data(path, all_numeric)
        self.num_features = len(self.all_data.T)-1
        self.num_samples = len(self.all_data)


    @numba.jit
    def load_data(self, path, all_numeric):
        if(all_numeric):
            if(self.token is not None):
                return np.loadtxt(path, delimiter=self.token)
            else:
                return np.loadtxt(path)  # read file into array
        else:
            if (self.token is not None):
                df = pd.read_csv(path, sep=self.token)
            else:
                df = pd.read_csv(path)
            arr = np.array(df)
            return arr



    """
    The scale() function returns scaled and preprocessed data
    The function takes optional arguments where
        + option determines the type of scaling/preprocessing applied to the data
        + num_labels is the number of labels or classes for classification problems
    """
    def scale(self, option=None, num_labels=1, labels=None):
        #if no option selected, just separate targets from inputs
        if(option == None):
            return self.cleave(labels=num_labels)
        # scale all data to [-1, 1]
        elif(option==0):
            self.all_data = pre.maxabs_scale(self.all_data)
            return self.cleave()
        # scale to unit normal distribution accounting for outliers
        elif(option==1):
            x, y = self.cleave(labels=num_labels)
            x = pre.robust_scale(x)
            return x, y
        #Multi-Label, categorical encoding for SVM
        # For multi-class classification
        elif(option==2):
            x, y = self.cleave(labels=num_labels)
            #preprocess y into binary labeled encoded matrix
            lb = pre.LabelEncoder()
            y = lb.fit_transform(np.ravel(y))
            print(lb.classes_)
            #scale x values
            x = pre.RobustScaler(quantile_range=(35.0, 65.0)).fit_transform(x)
            return x, y


    """
    The cleave() method separates data into an input vector and a target
    for regression and classification
    """
    def cleave(self, labels=1):
            x = copy.copy(self.all_data[:,0:-labels])
            y = copy.copy(self.all_data[:,-labels:])
            return x, y


    """
    The reload() method loads a new set of data into the DataHandler object
    """
    def reload(self, path=None, token=None, all_numeric=False):
        self.path = path
        self.token = token
        self.all_data = self.load_data(self.path, all_numeric)
