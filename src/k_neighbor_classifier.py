__author__ = 'joseph'

import prepare_data as prepare
import evaluate
from sklearn.neighbors import KNeighborsClassifier

train_x, train_y, validation_x, validation_y, test_data, basic_users_info, label_encoder = prepare.get_label_encode_data()

neighbor_classifier = KNeighborsClassifier(n_neighbors=11)

neighbor_classifier.fit(train_x, train_y)
validation_predict = neighbor_classifier.predict(validation_x)

predict_list = [[predict] for predict in validation_predict]

ndcg = evaluate.ndcg(predict_list, validation_y)
print(ndcg)

test_x = prepare.get_not_ndf_test_x(test_data, basic_users_info, label_encoder)
test_predict = neighbor_classifier.predict(test_x)
test_predict_list = [[predict] for predict in test_predict]
prepare.get_test_predict(test_data, test_predict_list)