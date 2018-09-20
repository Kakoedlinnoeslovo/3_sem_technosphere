
from utils import log_out, plot_graphs, DataReader
from carrot import Carrot

from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score
from tqdm import tqdm


seed = 10
np.random.seed(seed)



class Gradient_Boosting:
    def __init__(self, n_estimators=100, max_depth=10,
                 min_samples_split=1,
                 estimators_list = None,
                 global_leaf_numbers=None,
                 F = None, logistic_regression = None):

        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.estimators_list = estimators_list
        if estimators_list is None:
            self.estimators_list = list()

        self.F = F
        self.b = 0.5
        self.global_leaf_numbers = global_leaf_numbers
        self.logistic_regression = logistic_regression


    @staticmethod
    def _identify(pred, Y):
        return np.array([pred == Y]).astype(np.int8)


    def _compute_sample_weight(self, y, pred):
        return np.mean(np.exp(-(2. * y - 1.) * pred))


    def negative_gradient(self, y, pred):
        y_ = -(2. * y - 1.)
        return y_ * np.exp(y_ * pred - np.max(y_ * pred ))


    def _update_terminal_region(self, y, pred) :
        y_ = 2. * y - 1.
        for i in range(self.global_leaf_numbers.shape[1]):
            mask = self.global_leaf_numbers[:, i] == 1
            sample_weight = self._compute_sample_weight(y[mask], pred[mask])
            numerator = np.sum(y_[mask] * sample_weight * np.exp(-y_[mask] * pred[mask]))
            denominator = np.sum(sample_weight * np.exp(-y_[mask] * pred[mask]))
            if abs(denominator) < 1e-150:
                for i in np.where(mask)[0]:
                    self.global_leaf_numbers[i, np.where(self.global_leaf_numbers[i]!=0)[0][0]] = 0
            else:
                for i in np.where(mask)[0]:
                    self.global_leaf_numbers[i, np.where(self.global_leaf_numbers[i] != 0)[0][0]] = numerator / denominator


    def compute_antigrad(self, Y):
        Y_ = -(2. * Y - 1.)
        return Y_ * np.exp(-(Y_ * self.F) - np.max(Y_ * self.F))


    def fit(self, X, Y):
        if self.global_leaf_numbers is None:
            self.F = first_estimator = 0
            self.estimators_list.append(first_estimator)

        for i in range(len(self.estimators_list), self.n_estimators):
            antigrad = self.compute_antigrad(Y)
            antigrad = antigrad.astype(np.float64)
            new_estimator = Carrot(max_depth = self.max_depth)
            new_estimator.fit(X, antigrad)
            new_estimator_pred = new_estimator.predict(X)
            leaf_numbers = new_estimator.decision_path

            if self.global_leaf_numbers is not None:
               self.global_leaf_numbers = np.hstack((self.global_leaf_numbers, leaf_numbers))
            else:
                self.global_leaf_numbers = leaf_numbers

            self.F += self.b * new_estimator_pred
            self.estimators_list.append(new_estimator)

            logistic_regression = LogisticRegression(solver='newton-cg', max_iter=200)
            logistic_regression.fit(self.global_leaf_numbers, Y)
            predicted = logistic_regression.predict(self.global_leaf_numbers)

            self._update_terminal_region(Y, predicted)
            log_out(i, self.n_estimators, predicted , Y, antigrad, new_estimator_pred)
            self.logistic_regression = logistic_regression
        return self.estimators_list, self.F, self.global_leaf_numbers


    def predict(self, X):
        pred = self.estimators_list[0]
        total_leaf_numbers = None
        for estimator in self.estimators_list[1:]:
            temp_pred = estimator.predict(X)
            pred += self.b * temp_pred
            leaf_numbers = estimator.decision_path

            if total_leaf_numbers is not None:
                total_leaf_numbers = np.hstack((total_leaf_numbers, leaf_numbers))
            else:
                total_leaf_numbers = leaf_numbers

        predict = self.logistic_regression.predict(total_leaf_numbers)
        return predict


def unit_test():

    reader = DataReader()
    X_train, Y_train = reader.get(dtype = "train", ttype = "classification")
    X_test, Y_test = reader.get(dtype = "test", ttype = "classification")

    losses_my = list()
    losses_sklearn = list()
    trees_num = [x*10 for x in range(6,10)]

    #accuracy on train
    estimators_list = None
    global_leaf_numbers = None
    F = None
    for i in tqdm(trees_num):
        algo1 = Gradient_Boosting(n_estimators=i, min_samples_split=4, max_depth=3,
                                  estimators_list = estimators_list ,
                                  F = F,
                                  global_leaf_numbers = global_leaf_numbers)
        estimators_list, F, global_leaf_numbers  = algo1.fit(X_train, Y_train)
        acs = accuracy_score(Y_test, algo1.predict(X_test))
        losses_my.append(acs)
        print("my Accuracy: %.4f" % acs)

        algo = GradientBoostingClassifier(n_estimators=i,
                                         max_depth=3,
                                         min_samples_split=4,
                                         loss = "exponential")
        algo.fit(X_train, Y_train)
        acs = accuracy_score(Y_test, algo.predict(X_test))
        losses_sklearn.append(acs)
        print("sklearn Accuracy: %.4f" % acs)

    plot_graphs(trees_num, losses_my, losses_sklearn)


if __name__ == "__main__":
    unit_test()
