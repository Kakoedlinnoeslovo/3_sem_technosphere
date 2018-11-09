import pandas as pd
import numpy as np

class Reader:
    def __init__(self):
        pass

    def get_data(self, path):
        if 'train' in path:
            data = pd.read_csv(path, sep="\t", names=["User_id", "Item_id", "Score"])
        else:
            data = pd.read_csv(path, sep = "\t", names=["User_id", "Item_id"])

        data_matrix = data.as_matrix()
        max_user_id = max(data.User_id)
        max_item_id = max(data.Item_id)

        data_array = np.zeros((max_user_id, max_item_id))

        for elem in data_matrix:
            if 'train' in path:
                data_array[elem[0] - 1, elem[1] - 1] = elem[2]
            else:
                data_array[elem[0] - 1, elem[1] - 1] = 1

        return data_array

    def get_sample(self, sample_path):
        sample = pd.read_csv(sample_path, sep=",")
        return sample