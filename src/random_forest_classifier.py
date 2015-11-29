__author__ = 'joseph'

import prepare_data as prepare
import evaluate
from sklearn.ensemble import RandomForestClassifier

train_x, train_y, validation_x, validation_y, test_data, label_encoder = prepare.get_label_encode_data()

rf = RandomForestClassifier(n_estimators=11, criterion='gini')
rf.fit(train_x, train_y)
validation_predict = rf.predict(validation_x)

predict_list = [[predict] for predict in validation_predict]

ndcg = evaluate.ndcg(predict_list, validation_y)
print(ndcg)

