__author__ = 'joseph'

import prepare_data as prepare
import evaluate
import io_helper
from sklearn.neighbors import KNeighborsClassifier

train_data, validation_data, test_data, basic_users_info = prepare.get_data()
label_encoder = {}
train_x, train_y = prepare.get_exclude_ndf_x(train_data, basic_users_info, label_encoder)
validation_x, validation_y = prepare.get_exclude_ndf_x(validation_data, basic_users_info, label_encoder)

# max_ndcg = 0
# max_k = 0
# k_ndcg = {}
# for k in range(1, 100):
#     neighbor_classifier = KNeighborsClassifier(n_neighbors=k)
#     neighbor_classifier.fit(train_x, train_y)
#     validation_predict = neighbor_classifier.predict(validation_x)
#     predict_list = [[predict] for predict in validation_predict]
#
#     ndcg = evaluate.ndcg(predict_list, validation_data)
#     k_ndcg.setdefault(k, ndcg)
#     if ndcg > max_ndcg:
#         max_ndcg = ndcg
#         max_k = k
#         print(max_ndcg, max_k)
#
# io_helper.write_map_data(k_ndcg, '../records/k_neighbors_classifier.csv')
# (0.8724597056762439, 25)

neighbor_classifier = KNeighborsClassifier(n_neighbors=25)
neighbor_classifier.fit(train_x, train_y)

test_x = prepare.get_exclude_ndf_test_x(test_data, basic_users_info, label_encoder)
test_predict = neighbor_classifier.predict(test_x)
test_predict_list = [[predict] for predict in test_predict]
prepare.get_test_predict(test_data, test_predict_list)
