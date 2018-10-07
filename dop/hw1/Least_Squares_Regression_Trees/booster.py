from dop.hw1.utils import log_out, plot_graphs, DataReader, adaboost_loss
from dop.hw1.Least_Squares_Regression_Trees.carrot import Carrot

from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from sklearn.linear_model import LogisticRegression
from tqdm import tqdm
from random import shuffle


seed = 10
np.random.seed(seed)


class Booster:
    def __init__(self, n_estimators=100, max_depth=10,
                 min_samples_split=1,
                 estimators_list=None,
                 global_leaf_numbers=None,
                 F=None,
                 node_weights = None,
                 b = 0.5):


            self.n_estimators = n_estimators
            self.max_depth = max_depth
            self.min_samples_split = min_samples_split
            self.estimators_list = estimators_list
            if estimators_list is None:
                self.estimators_list = list()

            self.F = F
            self.b = b
            self.global_leaf_numbers = global_leaf_numbers
            self.node_weights = node_weights
            self.logistic_regression = None

    @staticmethod
    def _compute_antigrad(y, F):
        y_ = 2 * y - 1
        return y_ * np.exp(-y_ * F - np.max(y_ * F))


    @staticmethod
    def _compute_numerator_node(mask, y_, F, sample_weight):
        return np.sum(y_[mask] * sample_weight * np.exp(-y_[mask]*F[mask] - np.max(y_[mask]*F[mask])))


    @staticmethod
    def _compute_denominator_node(mask, y_, F, h, sample_weight):
        result = np.sum(sample_weight * np.exp(-y_[mask] * F[mask] - np.max(y_[mask]*F[mask])))
        return result


    def _compute_step(self, y, new_estimator_pred):
        y_ = 2. * y - 1.
        numerator = np.sum(y_*np.exp(-y_*new_estimator_pred - np.max(y_*new_estimator_pred)))
        denominator = np.sum(np.exp(-y_*new_estimator_pred - np.max(y_*new_estimator_pred)))
        result = numerator/denominator
        return result


    def _compute_sample_weight(self, y, pred):
        return np.mean(np.exp(-(2. * y - 1.) * pred - np.max((2. * y - 1.) * pred)))


    def _rescale_node(self, y, h, leaf_numbers):
        node_weights = np.ones(leaf_numbers.shape[1])
        answer = np.ones((len(y)))
        y_ = 2 * y - 1
        n = leaf_numbers.shape[1]
        for i in range(n):
            mask = leaf_numbers[:, i] == 1

            if len(y[mask]) == 0:
                continue

            sample_weight = self._compute_sample_weight(y[mask], h[mask])
            numerator = self._compute_numerator_node(mask, y_, self.F, sample_weight)
            denominator = self._compute_denominator_node(mask, y_, self.F, h, sample_weight)
            if abs(denominator) < 1e-150:
                for j in np.where(mask)[0]:
                    leaf_numbers[j,i] = 0
                    h[j]*=0
            else:
                for j in np.where(mask)[0]:
                    leaf_numbers[j,i] = numerator/denominator
                    h[j]*=numerator/denominator
                    answer[j] = numerator/denominator

                node_weights[i] = numerator/denominator
        self.node_weights.append(node_weights)
        return leaf_numbers, h, answer


    def fit(self, X, y):

        if self.global_leaf_numbers is None:
            self.F = first_estimator = np.zeros(y.shape)
            self.estimators_list.append(first_estimator)
            self.node_weights = list()

        for i in range(len(self.estimators_list), self.n_estimators):

            antigrad = self._compute_antigrad(y, self.F)
            new_estimator = Carrot(max_depth = self.max_depth)
            new_estimator.fit(X, antigrad)

            self.estimators_list.append(new_estimator)
            new_estimator_pred = new_estimator.predict(X)
            leaf_numbers = new_estimator.decision_path

            _, _, h = self._rescale_node(y, new_estimator_pred, leaf_numbers)

            self.logistic_regression = LogisticRegression()

            if self.global_leaf_numbers is not None:
               self.global_leaf_numbers = np.hstack((self.global_leaf_numbers, leaf_numbers))
            else:
                self.global_leaf_numbers = leaf_numbers


            self.logistic_regression.fit(self.global_leaf_numbers, y)

            log_out(estimator_number = i,
                    n_estimators = self.n_estimators,
                    pred = self.F, y = y,
                    error_func=adaboost_loss,
                    error_name="AdaboostLoss")

            self.F +=self.b * h

        return self.estimators_list, self.F, self.global_leaf_numbers, self.node_weights


    def predict(self, X):
        total_leaf_numbers = None
        for i, estimator in enumerate(self.estimators_list[1:]):
            _ = estimator.predict(X)
            leaf_numbers = estimator.decision_path
            for j in range(leaf_numbers.shape[1]):
                mask = leaf_numbers[:, j] == 1
                leaf_numbers[mask]*=self.node_weights[i][j]

            if total_leaf_numbers is not None:
                total_leaf_numbers = np.hstack((total_leaf_numbers, leaf_numbers))
            else:
                total_leaf_numbers = leaf_numbers

        predict = self.logistic_regression.predict(total_leaf_numbers)
        return predict


def unit_test():

    reader = DataReader()
    X_train, Y_train = reader.get(dtype="train", ttype="classification")
    X_test, Y_test = reader.get(dtype="test", ttype="classification")

    losses_my = list()
    losses_sklearn = list()
    trees_num = [10, 20, 30, 40] + [x * 50 for x in range(1, 8)]


    estimators_list = None
    global_leaf_numbers = None
    F = None
    node_weights = None
    b = 0.1

    ind_list = [i for i in range(len(X_train))]
    shuffle(ind_list)

    Y_test = Y_test * 2 - 1.

    for i in tqdm(trees_num):
        algo1 = Booster(n_estimators=i, min_samples_split=4, max_depth=3,
                                  estimators_list=estimators_list,
                                  F=F,
                                  global_leaf_numbers=global_leaf_numbers,
                                  node_weights= node_weights,
                        b = b)
        #b*=0.5
        estimators_list, F, global_leaf_numbers, node_weights = algo1.fit(X_train[ind_list, :],
                                                                          Y_train[ind_list])


        my_pred = algo1.predict(X_test)
        aloss = adaboost_loss(Y_test, my_pred)
        losses_my.append(aloss)
        print("\nmy AdaboostLoss: %.4f" % aloss)

        algo = GradientBoostingClassifier(n_estimators=i,
                                          max_depth=3,
                                          min_samples_split=4,
                                          loss="exponential")
        algo.fit(X_train, Y_train)
        sklearn_pred = algo.predict(X_test)
        aloss = adaboost_loss(Y_test, sklearn_pred)
        losses_sklearn.append(aloss)
        print("sklearn AdaboostLoss: %.4f" % aloss)

    plot_graphs(trees_num, losses_my, losses_sklearn)


if __name__ == "__main__":
    unit_test()