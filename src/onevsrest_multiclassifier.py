import prepare_data as prepare
import evaluate
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier

train_data, validation_data, test_data, basic_users_info = prepare.get_data()
label_encoder = {}
train_x, train_y = prepare.get_exclude_ndf_x(train_data, basic_users_info, label_encoder)
validation_x, validation_y = prepare.get_exclude_ndf_x(validation_data, basic_users_info, label_encoder)

rf = OneVsRestClassifier(RandomForestClassifier(n_estimators=11, criterion='gini')).fit(train_x, train_y)
validation_predict = rf.predict(validation_x)
validation_predict_proba = rf.predict_proba(validation_x)
# print validation_predict_proba
class_order = rf.classes_


# print validation_predict
def candidate_classes(predict):
	country = []
	for samples in predict:
		local = [i[0] for i in sorted(enumerate(samples), key = lambda x:x[1])]
		l = []
		for k in range(5):
			l.append(local[len(local) - k - 1])
		#print l
		country.append([class_order[j] for j in l])
	#print country
	return country

predict_list = candidate_classes(validation_predict_proba)

#print predict_list
ndcg = evaluate.ndcg(predict_list, validation_data)
print(ndcg)

test_x = prepare.get_exclude_ndf_test_x(test_data, basic_users_info, label_encoder)
test_predict = rf.predict(test_x)
test_predict_list = [[predict] for predict in test_predict]
prepare.get_test_predict(test_data, test_predict_list)
