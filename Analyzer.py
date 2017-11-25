import sklearn as sk
import DataHandler
import numpy as np
import PrintPlots as pp
from sklearn import neural_network as nn
from sklearn import model_selection as model


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
    A multilayer perceptron was used with 5x2 corss validation of the data to attempt to answer this question
    """
    def question_1(self):
        self.dh = DataHandler.DataHandler("q1.csv")
        #separate data into inputs and targets, x and y
        x, y = self.dh.cleave()
        #Create a Multilayer perceptron object that uses
        mlp = nn.MLPRegressor(hidden_layer_sizes=(2, 7), activation=('tanh'), solver='ibfgs')
        #cross-validation generator object from sklearn to use for crossvalidation
        cv_gen = model.RepeatedKFold()
        sizes, train_score , test_score = model.learning_curve(mlp,x, y, cv=cv_gen)
        pp.PrintPlots.print_learning_curve(sizes, train_score, test_score, title="MLP learning curve")