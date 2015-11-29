__author__ = 'joseph'

import prepare_data as prepare
import evaluate
from sklearn.ensemble import RandomForestClassifier

train_data, validation_data, test_data, basic_users_info = prepare.get_data()
label_encoder = {}
train_x, train_y = prepare.get_exclude_ndf_x(train_data, basic_users_info, label_encoder)
validation_x, validation_y = prepare.get_exclude_ndf_x(validation_data, basic_users_info, label_encoder)

rf = RandomForestClassifier(n_estimators=11, criterion='gini')
rf.fit(train_x, train_y)
validation_predict = rf.predict(validation_x)
predict_list = [[predict] for predict in validation_predict]

ndcg = evaluate.ndcg(predict_list, validation_data)
print(ndcg)

test_x = prepare.get_exclude_ndf_test_x(test_data, basic_users_info, label_encoder)
test_predict = rf.predict(test_x)
test_predict_list = [[predict] for predict in test_predict]
prepare.get_test_predict(test_data, test_predict_list)

