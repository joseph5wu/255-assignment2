__author__ = 'joseph'

import math


def ndcg(predict_list, y_list):
    total_dcg = 0
    for i in range(len(y_list)):
        predict = predict_list.get(i)
        result = y_list.get(i)
        for j in range(len(predict)):
            if predict.get(j) == result:
                total_dcg += float(1 / math.log(j + 2))
                break

    return total_dcg / len(y_list)
