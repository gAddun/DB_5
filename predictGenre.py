from __future__ import print_function
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import pandas as pd
import os
import subprocess

class createGenreTree:          #made into a class from my original format as standalone script
                                #makes it easier to call because it has its own methods
    def numerateCategorical(self,data, target_column):  #this changes the categorical field of genres to integers to work with sklearn
        coded=data.copy()
        targets= coded[target_column].unique()
        map_to_int={name: n for n, name in enumerate(targets)}
        coded["Target"] = coded[target_column].replace(map_to_int)
        return (coded, targets)

    def visualize_tree(self,tree, feature_names):   #this creates a dot file which can be turned into a picture with graphviz
        with open("DecTree.dot", 'w') as f:
            export_graphviz(tree, out_file=f,
                            feature_names=feature_names)    

        command = ["dot", "-Tpng", "DecTree.dot", "-o", "DecTree.png"]
        try:
            subprocess.check_call(command)
        except:
            exit("Could not run dot, ie graphviz, to "
                "produce visualization")

    def __init__(self):
        
        data=pd.read_csv("g2fix.csv")

        print("Data Head", data.head(), sep="\n", end="\n\n") #just fr printing out what data looks like at first couple rows (head)
        print("Data tail", data.tail(), sep="\n", end="\n\n") #last couple rows (tail)

        numData, targets = self.numerateCategorical(data, "Genres") #makes sklearn able to use data, doesnt handle strings well as far as i can tell

        print("Numerical data head", numData[["Target", "Genres"]].head(), #for debugging, shows what the categorical data is enumerated to
        sep="\n", end="\n\n")
        print("Numerical data tail", numData[["Target", "Genres"]].tail(),
        sep="\n", end="\n\n")
        print("targets", targets, sep="\n", end="\n\n") #all the genres it has

        features = list(numData.columns[:3])    #display features its working with
        print("features:", features, sep="\n")

        DecTree=DecisionTreeClassifier(min_samples_split=250, random_state=99) #Min samples split is most important tunable parameter
        #DecTree=DecisionTreeClassifier( random_state=99)   #Min samples split is at 250 because it was the most precise i could get the tree while being readable
        DecTree.fit(numData[features],numData["Target"])    #Lower splits leads to lower GINI impurity measures but drastically higher number of branches

        self.visualize_tree(DecTree,features)   #display the tree
