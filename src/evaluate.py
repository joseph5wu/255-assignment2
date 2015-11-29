__author__ = 'joseph'

import math
import load_data as load


def ndcg(predict_list, data):
    total_dcg = 0
    index = 0
    for user in data:
        destination = user[load.USERS_COUNTRY_DESTINATION]
        if destination == 'NDF':
            total_dcg += 1
        else:
            predicts = predict_list[index]
            for j in range(len(predicts)):
                if predicts[j] == destination:
                    total_dcg += float(1 / math.log(j + 2, 2))
                    break
            index += 1

    return total_dcg / len(data)

