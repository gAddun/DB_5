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
        + "Can we predict imdb score based on votes and revenue?"
    A multilayer perceptron was used with 5x2 corss validation of the data to attempt to answer this question
    """
    def question_1(self):
        self.dh = DataHandler.DataHandler("q1.csv", token=',')
        #separate data into scaled inputs and targets, x and y
        x, y = self.dh.scale(option=1)
        #Create a Multilayer perceptron object that uses
        mlp = nn.MLPRegressor(hidden_layer_sizes=(1, 8), activation=('tanh'), learning_rate_init=.01, solver='adam', warm_start=True)
        #cross-validation generator object from sklearn to use for crossvalidation
        cv_gen = model.RepeatedKFold()
        intervals = [.1, .2, .3, .4, .5, .6, .7, .8, .9, .99] # intervals for graph. measurements at percent relative to data size
        sizes, train_score, test_score = model.learning_curve(mlp, x, np.ravel(y), cv=cv_gen, train_sizes=intervals, scoring="r2")
        pp.PrintPlots.print_learning_curve(sizes, train_score, test_score, title="MLP learning curve")
        self.dh = None
