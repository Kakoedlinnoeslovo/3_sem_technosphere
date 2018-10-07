from dop.hw1.utils import find_best_split

import numpy as np
from sklearn.metrics import mean_squared_error as mse


class Oblivion:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.split_val = np.zeros(max_depth)
        self.split_idx = np.zeros(max_depth, np.int32)
        self.row_indexes = None
        self.pred_indexes = None
        self.answer = np.zeros(2**max_depth)


    def fit(self, X, y):
        self.row_indexes = np.zeros(y.shape[0])
        cant_see = list()
        for level in range(self.max_depth):
            b_gain, b_split_val, b_split_idx = -1, 0, 0
            for idx in range(X.shape[1]):
                split_val, gain = find_best_split(X, y, idx)
                if gain > b_gain and idx not in cant_see:
                    b_gain = gain
                    b_split_val = split_val
                    b_split_idx = idx

            self.split_val[level] = b_split_val
            self.split_idx[level] = b_split_idx
            cant_see.append(b_split_idx)
            self.row_indexes*=2
            self.row_indexes[X[:, b_split_idx] > b_split_val] +=1

        for leaf in range(2 ** self.max_depth):
            if len(y[self.row_indexes == leaf]) == 0:
                ans = 0
            else:
                ans = np.mean(y[self.row_indexes == leaf])
            self.answer[leaf] = ans


    def _get_indexes(self, X):
        indexes = np.zeros(X.shape[0])
        for level in range(self.max_depth):
            indexes *= 2
            indexes[X[:, self.split_idx[level]] > self.split_val[level]] +=1
        return indexes


    def predict(self, X):
        self.pred_indexes = self._get_indexes(X)
        answer = np.zeros((X.shape[0]))
        for leaf in range(2 ** self.max_depth):
            if self.answer[leaf]:
                answer[self.pred_indexes == leaf] = self.answer[leaf]
            else:
                answer[self.pred_indexes == leaf] = 0
        return answer


if __name__ == "__main__":
    tree = Oblivion(max_depth=3)
    X, y = np.random.randn(100, 4), np.random.randn(100)

    tree.fit(X, y)
    print(mse(tree.predict(X), y))





