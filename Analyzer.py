import sklearn as sk
import DataHandler
import numpy as np
import PrintPlots as pp
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn import svm
from sklearn.multioutput import MultiOutputClassifier
from sklearn import neural_network as nn
from sklearn import model_selection as model
from sklearn import feature_extraction
from sklearn import naive_bayes as nb



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
        x, y = self.dh.scale(option=0)
        #Create a Multilayer perceptron object that uses
        mlp = nn.MLPRegressor(hidden_layer_sizes=(1, 8), activation=('relu'), learning_rate_init=.1, solver='adam', warm_start=True)
        #cross-validation generator object from sklearn to use for crossvalidation
        cv_gen = model.RepeatedKFold()
        intervals = [.125, .25, .375, .5, .625, .75, .875] # intervals for graph. measurements at percent relative to data size
        sizes, train_score, test_score = model.learning_curve(mlp, x, np.ravel(y), cv=cv_gen, train_sizes=intervals, scoring="neg_mean_squared_error")
        pp.PrintPlots.print_learning_curve(sizes, train_score, test_score, title="MLP learning curve")
        self.dh = None

    """
    The question_3 function uses Support vector machine classification to answer the question:
        + How do the relationships between budget, duration and gross affect content rating?
    """

    def question_3_subroutine(self, title, axis1, axis2):
        self.dh = DataHandler.DataHandler(title, token=',', all_numeric=False)
        h = .02
        X, Y = self.dh.scale(option=2)
        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        classifier = svm.SVC(probability=True)
        y_prime = np.ravel(Y)
        classifier.fit(X, y_prime)
        Z = classifier.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
        Z = Z.reshape(xx.shape)
        # Put the result into a color plot
        pp.PrintPlots.contour_plot(Z, xx, yy, axis1, axis2)




    '''
    The question_4 function performs analysis to answer the question:
        + 'Can we predict the content rating of a film based on plot keywords'
    To accomplish this, we first extrapolate a TF-IDF(term frequency, inverse document frequency) matrix based on the vocabulary 'plot-keywrds'
    We then feed this vectorized data to a Multinomial Naive-Bayes classifier to train the classifier
    Finally, we feed our trained classifier some novel keywords and have the classifier predict content ratings
    '''
    def question_4(self):
        self.dh = DataHandler.DataHandler("q4.csv", token=',', all_numeric=False)
        x, y = self.dh.scale()
        labels = []
        for each in y:
            if (labels.count(each)<=0):
                labels.append(each)
        novel = ["sex murder pary", "mermaid dance party", "high school dancing",
                 "male frontal nudity", "brief female nudity",
                 "based true story", "based comic book", "Based on toy franchise",
                 "sequel", "prequel", "trilogy", "universe", "franchise",
                 "dog basketball", "basketball sports", "dog fighting",
                 "Science Fiction", "Science fiction military", "science fiction space", "science fiction time", "cyberpunk", "steampunk",
                 "college professor fights Nazis Jesus lazers",
                 "man with disability meets cool people does cool things",
                 "cat runs away lives with gay couple after father dies grows up returns home kills uncle",
                 "father tries to save his disabled son from a kidnapper",
                 "american invades foreign land kills local leadership struggles to find exit strategy",
                 "your 2006 Toyota Camry can shape shift with more explosions than dialogue",
                 "Troubled teen runs away to sleep with seven men in the same bed",
                 "doctor brings people closer together",
                 "interracial couple chased by man with burning cross",
                 "murderer takes on the identity of his victim"]
                #The last 9 novel phrases are movie plots explained poorly
                    #1 Indiana Jones
                    #2 Forest Gump
                    #3 Lion King
                    #4 Finding Nemo
                    #5 Wizard of Oz
                    #6 Transformers
                    #7 Snow White
                    #8 The human centipede
                    #9 Star Wars: The Force Awakens


        vectorizer = feature_extraction.text.TfidfVectorizer(max_df=0.33, min_df=1, stop_words='english',
                                                             ngram_range=(1, 2))
        x_prime = vectorizer.fit_transform(np.ravel(x))
        novel_prime = vectorizer.transform(np.ravel(novel))
        classifier = nb.MultinomialNB(alpha=0)
        classifier.fit(x_prime, y)
        predictions = classifier.predict(novel_prime)
        with open("predictions.csv", 'w') as file:
            for i in range(0, len(novel)):
                entry = ""
                entry += novel[i] + "," + predictions[i] + "\n"
                file.write(entry)
            file.close()





