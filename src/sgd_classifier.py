__author__ = 'joseph'

import prepare_data as prepare
import evaluate
from sklearn.linear_model import SGDClassifier

train_data, validation_data, test_data, basic_users_info = prepare.get_data()
label_encoder = {}
train_x, train_y = prepare.get_exclude_ndf_x(train_data, basic_users_info, label_encoder)
validation_x, validation_y = prepare.get_exclude_ndf_x(validation_data, basic_users_info, label_encoder)

clf = SGDClassifier(loss="hinge", penalty="l2")
clf.fit(train_x, train_y)
validation_predict = clf.predict(validation_x)
predict_list = [[predict] for predict in validation_predict]

ndcg = evaluate.ndcg(predict_list, validation_data)
print(ndcg)
