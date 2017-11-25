import numpy as np
import matplotlib.pyplot as plt

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
        train_std = -1*np.std(train, axis=1)
        test_mean = -1*np.mean(test, axis=1)
        test_std = -1*np.std(test, axis=1)
        plt.grid()
        plt.fill_between(size, (train_mean-train_std), (train_mean+train_std), alpha=.01, color="c")
        plt.fill_between(size, (test_mean - test_std), (test_mean + test_std), alpha=.01, color="r")
        plt.plot(size, train_mean, 'o-', color="c",label="Training score")
        plt.plot(size, test_mean, 'o-', color="r",label="Cross-validation score")
        plt.legend(loc="best")
        file_name = "{}.png".format(title)
        fig.savefig(file_name)
        plt.close(fig)