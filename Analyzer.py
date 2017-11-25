import sklearn as sk
import DataHandler
import numpy as np


"""
The Analyzer class is responsible for performing analysis on the data extracted from our database
The methods question_1 - question_5 performs analyses related to the 5 questions we seek to answer for this project
"""
class Analyzer:
    #initializes the Analyzer object
    def __init__(self):
        # Analyzer has an instance of the DataHandler class. Initially set to null
        self.dh = None

    def question_1(self):
        self.dh = DataHandler.DataHandler("q1.csv", scaled=True)
