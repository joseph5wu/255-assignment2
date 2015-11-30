import prepare_data as prepare
import evaluate
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.multiclass import OneVsRestClassifier

train_data, validation_data, test_data, basic_users_info = prepare.get_data()
label_encoder = {}
train_x, train_y = prepare.get_exclude_ndf_x(train_data, basic_users_info, label_encoder)
validation_x, validation_y = prepare.get_exclude_ndf_x(validation_data, basic_users_info, label_encoder)

ndcg_list = []
for i in range(1, 50):
	rf = OneVsRestClassifier(GradientBoostingClassifier(learning_rate=0.05, n_estimators=i)).fit(train_x, train_y)
	validation_predict_proba = rf.predict_proba(validation_x)
	class_order = rf.classes_
	predict_list = evaluate.candidate_classes(validation_predict_proba, class_order)
	ndcg = evaluate.ndcg(predict_list, validation_data)
#print ndcg
	#ndcg_list.append(ndcg)
	print i, " ", ndcg

test_x = prepare.get_exclude_ndf_test_x(test_data, basic_users_info, label_encoder)
test_predict = rf.predict_proba(test_x)
test_predict_list = evaluate.candidate_classes(test_predict, class_order)
prepare.get_test_predict(test_data, test_predict_list)
