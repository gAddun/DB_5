from __future__ import print_function
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import pandas as pd
import os
import subprocess

class createGenreTree:
    def numerateCategorical(self,data, target_column):
        coded=data.copy()
        targets= coded[target_column].unique()
        map_to_int={name: n for n, name in enumerate(targets)}
        coded["Target"] = coded[target_column].replace(map_to_int)
        return (coded, targets)

    def visualize_tree(self,tree, feature_names):
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

        print("Data Head", data.head(), sep="\n", end="\n\n")
        print("Data tail", data.tail(), sep="\n", end="\n\n")

        numData, targets = self.numerateCategorical(data, "Genres") #makes sklearn able to use data, doesnt handle strings well as far as i can tell

        print("Numerical data head", numData[["Target", "Genres"]].head(),
        sep="\n", end="\n\n")
        print("Numerical data tail", numData[["Target", "Genres"]].tail(),
        sep="\n", end="\n\n")
        print("targets", targets, sep="\n", end="\n\n")

        features = list(numData.columns[:3])
        print("features:", features, sep="\n")

        DecTree=DecisionTreeClassifier(min_samples_split=250, random_state=99) #Tune these
        #DecTree=DecisionTreeClassifier( random_state=99)
        DecTree.fit(numData[features],numData["Target"])

        self.visualize_tree(DecTree,features)
