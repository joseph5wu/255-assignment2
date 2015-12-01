__author__ = 'valoria'

import prepare_data as prepare
import evaluate
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier


train_x, train_y, validation_x, validation_y, test_data, basic_users_info, label_encoder = prepare.get_label_encode_data()

#OneVsRestClassifier(LinearSVC(random_state=0)).fit(X, y).predict(X)

"""
rf = OneVsRestClassifier(RandomForestClassifier(n_estimators=11, criterion='gini'))
rf.fit(train_x, train_y)
validation_predict = rf.predict(validation_x)
"""
"""
neigh = KNeighborsClassifier(n_neighbors=11)
neigh.fit(train_x, train_y)
validation_predict = neigh.predict(validation_x)
"""
clf = AdaBoostClassifier(n_estimators=11)
clf.fit(train_x, train_y)
validation_predict = clf.predict(validation_x)

predict_list = [[predict] for predict in validation_predict]

ndcg = evaluate.ndcg(predict_list, validation_y)
print(ndcg)
