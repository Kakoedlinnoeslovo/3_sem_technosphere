from dop.hw1.MatrixNet.ObliviousTree import Oblivion
from dop.hw1.utils import plot_graphs
from dop.hw1.utils import DataReader, log_out

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error as MSE
import numpy as np

seed = 10
np.random.seed(seed)


class Gradient_Boosting:
    def __init__(self, learning_rate=0.1, n_estimators=100, max_depth=10,
                 min_samples_split=1, estimators_list = None, current_predict = None):
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.estimators_list = estimators_list

        if estimators_list is None:
            self.estimators_list = list()
        self.current_predict = current_predict


    def _rescale_node(self, pred, leaf_indexes, N):
        for leaf in range(2 ** self.max_depth):
            pred[leaf_indexes == leaf] *= np.sqrt(N/(N + len(pred[leaf_indexes == leaf])))
        return pred


    def fit(self, X, y):
        N = len(y)
        if self.current_predict is None:
            first_estimator = np.average(y)
            self.estimators_list.append(first_estimator)
            self.current_predict = first_estimator

        for i in range(len(self.estimators_list), self.n_estimators):
            antigrad = y - self.current_predict
            new_estimator = Oblivion(max_depth = self.max_depth)
            new_estimator.fit(X, antigrad)
            new_estimator_pred = new_estimator.predict(X)
            new_estimator_pred  = self._rescale_node(new_estimator_pred, new_estimator.row_indexes, N)
            learning_rate = self.learning_rate -  (self.learning_rate*(i+1)/self.n_estimators)*0.01
            self.current_predict += learning_rate * new_estimator_pred
            self.estimators_list.append(new_estimator)

            log_out(estimator_number=i,
                    n_estimators = self.n_estimators,
                    pred= self.current_predict,
                    y = y,
                    error_func = MSE,
                    error_name = "MSE")

        return self.estimators_list, self.current_predict


    def predict(self, X):
        y = self.estimators_list[0]
        N = len(X)
        for i, estimator in enumerate(self.estimators_list[1:]):
            learning_rate = self.learning_rate - (self.learning_rate * (i + 1) / self.n_estimators) * 0.01
            estimator_pred = estimator.predict(X)
            estimator_pred = self._rescale_node(estimator_pred, estimator.pred_indexes, N)
            y += estimator_pred * learning_rate
        return y


def unit_test():
    reader = DataReader()
    X_train, y_train = reader.get(dtype="train", ttype="regression")
    X_test, y_test = reader.get(dtype="test", ttype="regression")


    losses_my = list()
    print(X_train.shape, y_train.shape)
    losses_sklearn = list()
    trees_num = [x*10 for x in range(1,11)]
    #mse on train
    estimators_list = None
    current_predict = None
    for i in trees_num:
        algo1 = Gradient_Boosting(n_estimators=i, min_samples_split=4, max_depth=3,
                                  estimators_list =estimators_list ,
                                  current_predict= current_predict)
        y_TRAIN = np.copy(y_train)
        x_TRAIN = np.copy(X_train)
        estimators_list, current_predict = algo1.fit(X_train, y_train.ravel())
        mse = MSE(y_test, algo1.predict(X_test))
        losses_my.append(mse)
        print("\nmy MSE: %.4f" % mse)


        algo = GradientBoostingRegressor(n_estimators=i,
                                         criterion="mse",
                                         max_depth=3,
                                         min_samples_split=4)
        algo.fit(x_TRAIN, y_TRAIN.ravel())
        mse = MSE(y_test, algo.predict(X_test))
        losses_sklearn.append(mse)
        print("sklearn MSE: %.4f" % mse)

    plot_graphs(trees_num, losses_my, losses_sklearn, error_name = "MSE")


if __name__ == "__main__":
    unit_test()
