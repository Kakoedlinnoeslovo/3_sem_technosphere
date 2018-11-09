import numpy as np
from collections import defaultdict
from Reader import Reader
from tqdm import tqdm

np.random.seed(777)



class IALS:
    def __init__(self, max_user, max_item,
                 alpha = 10, eps = 0.1, emb_size = 15,
                 l2_reg = 0.1, max_epoch = 10):

        self.alpha = alpha
        self.eps = eps
        self.emb_size = emb_size
        self.l2_reg = l2_reg
        self.max_epoch = max_epoch
        self.max_user = max_user
        self.max_item = max_item
        self.result_matrix = None

    @staticmethod
    def _get_confidence(R, alpha, eps):
        return np.ones(R.shape) + alpha * np.log(np.ones(R.shape) + R / eps)


    def fit(self, X_train):
        """
        :param X:
            row - user
            column - item
        :return
        """

        assert X_train.shape[0] == self.max_user and \
                X_train.shape[1] ==self.max_item,\
                """Shape of X_train must be (max_user, max_item), 
                where X_train[max_user, max_item] = score"""

        #init
        P = X_train > 0
        C = self._get_confidence(X_train, self.alpha, self.eps)
        l2I = np.eye(self.emb_size, self.emb_size) * self.l2_reg
        X = np.random.random_sample((X_train.shape[0], self.emb_size))
        Y = np.random.random_sample((X_train.shape[1], self.emb_size))

        for epoch in tqdm(range(self.max_epoch)):
            for u in range(X.shape[0]):
                # formula  = (Y.T *C^{u}*Y + l2I)^{-1} * Y.T * C^{u} * p(u)
                first_bracket_left = np.matmul(Y.T *C[u, :], Y)
                first_bracket = first_bracket_left + l2I
                first_bracket_inv = np.linalg.inv(first_bracket)
                result = np.matmul(first_bracket_inv, Y.T) #shape = (emb_size, max_items)
                Cp = (C[u, :] * P[u,:]).reshape(-1, 1) #shape = (max_items, 1)
                result = np.matmul(result, Cp) #shape = (emb_size, 1)
                X[u, :] = result.ravel()

            for i in range(Y.shape[1]):
                #formula = (X.T* C^{i} *X + l2I)^{-1} * X.T * C^{i} * p(i)
                first_bracket_left = np.matmul(X.T * C[:, i], X)
                first_bracket = first_bracket_left + l2I
                first_bracket_inv = np.linalg.inv(first_bracket)
                result = np.matmul(first_bracket_inv, X.T)
                Cp = (C[:, i] * P[:, i]).reshape(-1, 1)
                result = np.matmul(result, Cp)
                Y[i, :] = result.ravel()

        self.result_matrix = np.matmul(X, Y.T)


    def predict(self, X_test):

        assert self.result_matrix is not None, "first fit"

        max_user_test = X_test.shape[0]
        max_item_test = X_test.shape[1]

        predicted = defaultdict(dict)


        for u in range(max_user_test):
            for i in range(max_item_test):
                if X_test[u, i] == 1:
                    if (len(predicted[u + 1]) == 0):
                        predicted[u + 1] = {i + 1: self.result_matrix[u, i]}
                    else:
                        predicted[u + 1][i + 1] = self.result_matrix[u, i]
                else:
                    continue
        return predicted


    def get_submit(self, sample_path, test_path, predicted):
        assert isinstance(predicted, defaultdict), \
            "predicted should be defaultdict"

        reader = Reader()

        sample_pd = reader.get_sample(sample_path)

        score_list = list()
        with open(test_path, "r") as test_file:
            lines = test_file.readlines()
            for line in lines:
                temp_user, temp_item = int(line.split("\t")[0]), \
                                       int(line.split("\t")[1])

                temp_score = predicted[temp_user][temp_item]
                score_list.append(temp_score)

        sample_pd.Score = score_list
        return sample_pd




