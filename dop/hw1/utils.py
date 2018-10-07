import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys


class DataReader:
    def __init__(self):
        self.rf_train = './dop/hw1/data/reg.train.txt'
        self.rf_test = './dop/hw1/data/reg.test.txt'

        self.cf_train = '.dop/data/spam.train.txt'
        self.cf_test = './dopdata/spam.test.txt'


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
                eps = 0.01
                X = (X - mean) / (std + eps)
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


def plot_graphs(trees_num, losses_my, losses_sklearn, error_name = "AdaboostLoss"):
    fig = plt.figure()
    fig.suptitle('{} от n_estimators'.format(error_name), fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('n_estimators')
    ax.set_ylabel("{}".format(error_name))
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


def log_out(estimator_number, n_estimators, pred, y, error_func, error_name = "AdaboostLoss"):
    sys.stderr.write('\rLearning estimator number: ' + str(estimator_number) + "/" + str(n_estimators) \
                     + "; {} error on train dataset: ".format(error_name) + str(error_func(pred, y)))



def find_best_split(X, y, col):
    sorted_indexes = np.argsort(X[:, col])
    N = len(y)
    S = np.sum(y)
    Sr = S
    Nr = N
    Sl = 0
    Nl = 0
    BestTillNow = 0
    BestCutPoint = 0
    y_sorted = y[sorted_indexes]
    X_sorted = X[sorted_indexes]

    for i in range(N - 1):
        Sl = Sl + y_sorted[i]
        Sr = Sr - y_sorted[i]
        Nl+=1
        Nr-=1
        if X_sorted[i+1, col] > X_sorted[i, col]:
            NewSplitValue = float(Sl**2)/Nl + float(Sr**2)/Nr
            if NewSplitValue > BestTillNow:
                BestTillNow = NewSplitValue
                BestCutPoint = float(X_sorted[i+1, col] + X_sorted[i, col]) /2

    return BestCutPoint, BestTillNow