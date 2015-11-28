__author__ = 'joseph'

import prepare_data as prepare
from sklearn.ensemble import RandomForestClassifier

train_x, train_y, validation_x, validation_y, test_data, label_encoder = prepare.get_label_encode_data()

rf = RandomForestClassifier(n_estimators=100, criterion='gini')
rf = rf.fit(train_x, train_y)
validation_predict = rf.predict(validation_x)
