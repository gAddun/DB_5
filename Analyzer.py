import sklearn as sk
import DataHandler
import numpy as np
from sklearn import neural_network as nn


"""
The Analyzer class is responsible for performing analysis on the data extracted from our database
The methods question_1 - question_5 performs analyses related to the 5 questions we seek to answer for this project
"""
class Analyzer:
    #initializes the Analyzer object
    def __init__(self):
        # Analyzer has an instance of the DataHandler class. Initially set to null
        self.dh = None


    """
    The question_1 function uses the sklearn MLPRegressor to answer question 1:
        "can we predict imdb score based on votes and revenue?"
    """
    def question_1(self):
        self.dh = DataHandler.DataHandler("q1.csv", scaled=True)
        x, y = self.dh.scale()
        mlp = nn.MLPRegressor(hidden_layer_sizes=(2, 7), activation=('tanh'), solver='ibfgs', )