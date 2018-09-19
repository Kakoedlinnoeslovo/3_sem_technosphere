import numpy as np
from tqdm import tqdm
from sklearn.metrics import mean_squared_error as mse

from utils import DataReader

class Carrot:
    def __init__(self, max_depth, min_samples_split = 2, min_samples_leaf = 1):
        """
        :param max_depth: The maximum depth of the tree.
        If None, then nodes are expanded until all leaves are pure or
        until all leaves contain less than min_samples_split samples.
        :param min_samples_split: The minimum number of samples required to split an internal node.
        :param min_samples_leaf: The minimum number of samples required to be at a leaf node.
        :param min_impurity_decrease: Threshold for early stopping in tree growth.
        """

        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.answer = None
        self.left = None
        self.right = None
        self.feature_val = None
        self.col = None
        self.decision_path = None


    @staticmethod
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


    def fit(self, X, y):
        N = len(y)
        mu = np.mean(y)
        Err = np.sum((y - mu)**2)/N
        CutPoint = None
        Col = None

        for col in range(X.shape[1]):
            BestCutPoint, Err_lr = self.find_best_split(X, y, col)
            if (Err_lr > Err):
                Err = Err_lr
                CutPoint = BestCutPoint
                Col = col

        self.feature_val = CutPoint
        self.col = Col

        if Col is None or N < self.min_samples_leaf or self.max_depth == 0:
            self.left = None
            self.right = None
            self.answer = np.mean(y)
            return


        if CutPoint is not None:
            Xl, yl, Xr, yr = X[X[:, Col] < CutPoint], y[X[:, Col] < CutPoint],\
                                                       X[X[:, Col] >= CutPoint], y[X[:, Col] >= CutPoint]

            self.left = Carrot(self.max_depth - 1, self.min_samples_split,
                               self.min_samples_leaf)
            self.right  = Carrot(self.max_depth - 1, self.min_samples_split,
                               self.min_samples_leaf)

            if (len(yl) < self.min_samples_split) and (len(yr) < self.min_samples_split):
                self.answer = np.mean(y)

            if (len(yl) > self.min_samples_split):
                self.left.fit(Xl, yl)
            else:
                self.left.answer = np.mean(yl)

            if (len(yr) > self.min_samples_split):
                self.right.fit(Xr, yr)
            else:
                self.right.answer = np.mean(yr)


    def _predict_single(self, x, position):

        if self.answer is None:
            if (x[self.col] < self.feature_val):
                position = position[:int(len(position)/2)]
                return self.left._predict_single(x, position)
            else:
                position = position[int(len(position)/2):]
                return self.right._predict_single(x, position)
        else:
            return self.answer, position[0]


    def predict(self, X):
        predictions = np.zeros((X.shape[0]))
        self.decision_path = np.zeros((X.shape[0], 2**self.max_depth))
        for i, x in enumerate(X):
            position = np.array([x for x in range(2 ** self.max_depth)])
            predictions[i], position = self._predict_single(x, position)
            return_position = np.zeros((2**self.max_depth))
            return_position[position] = 1
            self.decision_path[i] = return_position
        return predictions





def unit_test():
    reader = DataReader()
    X_train, y_train = reader.get(dtype = "train", ttype = "regression")
    X_test, y_test = reader.get(dtype = "test", ttype = "regression")
    tree = Carrot(max_depth=3)
    tree.fit(X_train, y_train)
    y_pred  = tree.predict(X_train)
    print(tree.decision_path)
    print("MSE on Train dataset is : {}".format(mse(y_train, y_pred)))
    y_pred  = tree.predict(X_test)
    print("MSE on Test dataset is : {}".format(mse(y_test, y_pred)))

if __name__ == "__main__":
    unit_test()


