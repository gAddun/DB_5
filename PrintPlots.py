import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import NullFormatter
from time import time
from itertools import cycle, islice

class PrintPlots:

    """
    This method saves a plot of the learning curve of a model as a png file
    """
    @staticmethod
    def print_learning_curve(size, train, test, title="no title"):

        fig = plt.figure()
        plt.title(title)
        plt.xlabel("Training iterations")
        plt.ylabel("Loss")
        train_mean = -1*np.mean(train, axis=1)
        test_mean = -1*np.mean(test, axis=1)
        plt.grid()
        plt.fill_between(size, (train_mean), (train_mean), alpha=.01, color="c")
        plt.fill_between(size, (test_mean), (test_mean), alpha=.01, color="r")
        plt.plot(size, train_mean, 'o-', color="c",label="Training score")
        plt.plot(size, test_mean, 'o-', color="r",label="Cross-validation score")
        plt.legend(loc="best")
        file_name = "{}.png".format(title)
        fig.savefig(file_name)
        plt.close(fig)

    @staticmethod
    def print_clusters(plt1, pred, true):
        fig = plt.figure()
        plt.title("Clusters")
        colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
                                             '#f781bf', '#a65628', '#984ea3',
                                             '#999999', '#e41a1c', '#dede00']),
                                      int(max(pred) + 1))))
        plt.scatter(plt1[:, 0], plt1[:, 1], s=10, color=colors[pred])
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        plt.xticks(())
        plt.yticks(())
        file_name = "Predicted.png"
        fig.savefig(file_name)
        plt.close(fig)

        fig = plt.figure()
        plt.title("Clusters VS labels")
        plt.scatter(plt1[:, 0], plt1[:, 1], s=10, color=colors[true])
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        plt.xticks(())
        plt.yticks(())
        file_name = "classes.png"
        fig.savefig(file_name)
        plt.close(fig)

    #Plot countours for classification areas for classification problems
    @staticmethod
    def contour_plot(Z, xx, yy, axis1, axis2):
        fig = plt.figure()
        colmap = ListedColormap(['g', 'r', 'b', 'olive', 'orchid', 'cyan', 'darkorange', 'magenta'])

        plt.contourf(xx, yy, Z, cmap=colmap, alpha=.8)
        #plt.scatter(X[:, 0], X[:, 1], color="k", edgecolors='k')
        plt.xlabel(axis1)
        plt.ylabel(axis2)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.xticks(())
        plt.yticks(())
        plt.legend(loc="best")
        file_name = "contour3.png"
        fig.savefig(file_name)
        plt.close(fig)




