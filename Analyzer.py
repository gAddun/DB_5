import sklearn as sk
import DataHandler
import numpy as np
import PrintPlots as pp
from sklearn import cluster
from sklearn import neural_network as nn
from sklearn import model_selection as model
from sklearn import feature_extraction
from sklearn import preprocessing as pre
from sklearn import decomposition as decomp
from sklearn import pipeline as pipe



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
    A multilayer perceptron was used with 5x2 cross validation of the data to attempt to answer this question
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

    '''
    The question_4 function performs analysis to answer the question:
        + 'Can we predict the content rating of a film based on plot keywords'
    To accomplish this, we first extrapolate a TF-IDF(term frequency, inverse document frequency) matrix based on the vocabulary 'plot-keywrds'
    We then apply spectral clustering to group the data in a 2d-plot
    For a comparison, we show the 3 graphs of the clustered data:
        1 with the data colored by cluster grouping, 1 with the data colored by class label and 1 with the obtained clusters and some novel combination of plot keywords fitted to the clusters
    '''
    def question_4(self):
        self.dh = DataHandler.DataHandler("q4.csv", token=',', all_numeric=False)
        #separate data into labels and features
        x, y = self.dh.scale()
        #analyze
        labels = []
        for each in y:
            if (labels.count(each)<=0):
                labels.append(each)
        #Encode labels (content rating)
        le = pre.LabelEncoder()
        encoded_y = le.fit_transform(np.ravel(y))
        novel = ["sex murder pary", "mermaid dance party", "high school party", "wizard talking animal", "male frontal nudity", "laser space elf", "dog basketball"]
        vectorizer = feature_extraction.text.TfidfVectorizer(max_df=0.25,min_df=1, stop_words='english', ngram_range=(1,2))
        x_prime = vectorizer.fit_transform(np.ravel(x))
        novel_prime = vectorizer.transform(novel)
        # cluster the data
        clusterer = cluster.KMeans(n_clusters=len(labels), init='random')
        C1 = clusterer.fit_predict(x_prime)  # Clustering of data points by plot keywords
        C2 = clusterer.predict(novel_prime)  # Clustering of novel data
        # Scale the data to 2 dimensions for visualization
        pca = decomp.KernelPCA(n_components=2)
        x_grid = pca.fit_transform(x_prime)
        novel_grid = pca.transform(novel_prime)


        pp.PrintPlots.print_clusters(x_grid, novel_grid, C1, encoded_y, C2)




