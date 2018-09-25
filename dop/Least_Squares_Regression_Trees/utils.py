import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, mean_squared_error
from tqdm import tqdm
import sys


class DataReader:
    def __init__(self):
        self.rf_train = 'data/reg.train.txt'
        self.rf_test = 'data/reg.test.txt'

        self.cf_train = 'data/spam.train.txt'
        self.cf_test = 'data/spam.test.txt'


    def get(self, dtype = "train", ttype = "regression"):
        if ttype == "regression":
            print("Start reading data ...")
            fpath = self.rf_train

            if dtype == "test":
                fpath = self.rf_test

            y, X = [], []
            with open(fpath, "r") as file:
                for line in file:
                    temp = []
                    for i in range(246):
                        temp.append(0)
                    line_sep = line.split()
                    y.append(float(line_sep[0]))
                    line_sep.pop(0)
                    for elem in line_sep:
                        buf = elem.split(':')
                        temp[int(buf[0])] = float(buf[1])
                    X.append(temp)

                y = np.array(y)
                X = np.array(X)
                print("End reading data ...")

                print("Normalising data ...")
                mean = X.mean(axis=0)
                std = X.std(axis=0)
                X = (X - mean) / std
                return X, y

        if ttype == "classification":
            print("Start reading data ...")
            x_list = list()
            y_list = list()
            fpath = self.cf_train

            if dtype == "test":
                fpath = self.cf_test

            with open(fpath, "r") as file:
                for line in tqdm(file.readlines()):
                    temp_line = line.split()
                    y_list.append(int(temp_line[0]))
                    x_list.append([float(x) for x in temp_line[1:]])

            X = np.array(x_list)
            y = np.array(y_list).astype(np.int8)
            print("End reading data ...")

            print("Normalising data ...")
            mean = X.mean(axis=0)
            std = X.std(axis=0)
            X = (X - mean) / std
            return X, y


def plot_graphs(trees_num, losses_my, losses_sklearn):
    fig = plt.figure()
    fig.suptitle('AdaboostLoss от n_estimators', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('n_estimators')
    ax.set_ylabel("AdaboostLoss")
    plt.grid()
    ax.plot(trees_num, losses_my, label="My Gradient Boosting")
    ax.plot(trees_num, losses_sklearn, label="Sklearn")
    plt.legend(loc="best")
    plt.fill_between(trees_num, np.array(losses_sklearn) - np.mean(losses_sklearn) * 0.03,
                     np.array(losses_sklearn) + np.mean(losses_sklearn) * 0.03,
                     alpha=0.1,
                     color="g")
    plt.show()


def adaboost_loss(y_pred, y):
    return np.mean(np.exp(- y_pred * y))


def log_out(i, n_estimators, current_predict, Y, antigrad, y_pred_reg):
    sys.stderr.write('\rLearning estimator number: ' + str(i) + "/" + str(n_estimators) \
                     + "; AdaboostLoss error on train dataset: " + str(adaboost_loss(current_predict, Y)) \
                 + "; MSE error on train dataset: {}".format(mean_squared_error(antigrad, y_pred_reg)))