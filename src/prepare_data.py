__author__ = 'joseph'

import load_data as load
import random
import csv
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import f_classif


def get_data():
    # load data from train set
    users_data, users_dict = load.get_train_users_data()
    test_users_data, test_users_dict = load.get_test_users_data()
    # shuffle the data and split the data into training set and validation set
    random.seed(0)
    random.shuffle(users_data)
    users_data_size = len(users_data)

    basic_users_info = get_basic_users_info(users_data)

    train_data = users_data[:users_data_size * 9 / 10]
    validation_data = users_data[users_data_size * 9 / 10:]
    test_data = test_users_data

    return train_data, validation_data, test_data, basic_users_info


def label_encode(data, label_encoder):
    for i in range(len(data[0])):
        if type(data[0][i]) is str:
            if i not in label_encoder:
                label_encoder[i] = {}
            for datum in data:
                value = datum[i]
                if value not in label_encoder[i]:
                    label_encoder[i][value] = len(label_encoder[i]) + 1
                    datum[i] = label_encoder[i][value]
                else:
                    datum[i] = label_encoder[i][value]


def get_basic_users_info(user_data):
    age_total = 0
    age_count = 0
    for user in user_data:
        age = user[load.USERS_AGE]
        if age is not None and age != '':
            age_total += float(age)
            age_count += 1

    return [age_total / age_count]


def get_record(user, basic_users_info):
    # parse timestamp_first_active into day month year
    timestamp_first_active = user[load.USERS_TIMESTAMP_FIRST_ACTIVE]
    year = int(timestamp_first_active[:4])
    month = int(timestamp_first_active[4:6])
    day = int(timestamp_first_active[6:8])

    date_first_booking = user[load.USERS_DATE_FIRST_BOOKING].strip().split('-')
    book_year = int(date_first_booking[0])
    book_month = int(date_first_booking[1])
    book_day = int(date_first_booking[2])

    gender = user[load.USERS_GENDER]
    age = user[load.USERS_AGE]
    if age is None or age == '':
        age = basic_users_info[0]
    else:
        age = float(age)

    signup_method = user[load.USERS_SIGNUP_METHOD]
    language = user[load.USERS_LANGUAGE]
    affiliate_provider = user[load.USERS_AFFILIATE_PROVIDER]
    first_device_type = user[load.USERS_FIRST_DEVICE_TYPE]
    first_browser = user[load.USERS_FIRST_BROWSER]

    # testing features
    date_account_created = user[load.USERS_DATE_ACCOUNT_CREATED].strip().split('-')
    created_year = int(date_account_created[0])
    created_month = int(date_account_created[1])
    created_day = int(date_account_created[2])
    signup_flow = int(user[load.USERS_SIGNUP_FLOW])
    affiliate_channel = user[load.USERS_AFFILIATE_CHANNEL]
    first_affiliate_tracked = user[load.USERS_FIRST_AFFILIATE_TRACKED]
    signup_app = user[load.USERS_SIGNUP_APP]

    return [month, book_month, age, language,
            affiliate_provider, first_device_type, first_browser]
    # [year, month, book_year, book_month, gender, age, signup_method, language,
    #         affiliate_provider, first_device_type, first_browser]
    # return [year, affiliate_channel, month, first_device_type, book_year, first_affiliate_tracked, book_month,
    #         first_browser, gender, age, language, affiliate_provider, created_year, created_month,
    #         signup_flow, signup_app, signup_method]


def get_exclude_ndf_x(data, basic_users_info, label_encoder):
    x = []
    y = []
    for user in data:
        destination = user[load.USERS_COUNTRY_DESTINATION]
        if destination == 'NDF':
            continue
        x.append(get_record(user, basic_users_info))
        y.append(destination)

    label_encode(x, label_encoder)
    return x, y


def get_exclude_ndf_test_x(test_data, basic_users_info, label_encoder):
    test_x = []
    for user in test_data:
        date_first_booking = user[load.USERS_DATE_FIRST_BOOKING]
        if date_first_booking is None or date_first_booking == '':
            continue
        test_x.append(get_record(user, basic_users_info))

    label_encode(test_x, label_encoder)
    return test_x


def get_test_predict(test_data, test_predict):
    with open('../data/test_predict.csv', 'wb') as predict_file:
        writer = csv.writer(predict_file)
        writer.writerow(['id', 'country'])
        index = 0
        for data in test_data:
            user_id = data[load.USERS_ID]
            date_first_booking = data[load.USERS_DATE_FIRST_BOOKING]
            if date_first_booking is None or date_first_booking == '':
                writer.writerow([user_id, 'NDF'])
            else:
                predict_list = test_predict[index]
                for predict in predict_list:
                    writer.writerow([user_id, predict])
                index += 1


def remove_features_with_low_variance(x_data):
    variance = VarianceThreshold(threshold=1.4)
    print ('before transform', len(x_data[4]), x_data[4])
    variance.fit(x_data)
    transformed_x = variance.transform(x_data)
    print ('after transform', len(transformed_x[4]), transformed_x[4])


def compute_f_value(x_data, y_data):
    F, pval = f_classif(x_data, y_data)
    print(F, pval)

# train_data, validation_data, test_data, basic_users_info = get_data()
# label_encoder = {}
# train_x, train_y = get_exclude_ndf_x(train_data, basic_users_info, label_encoder)
# remove_features_with_low_variance(train_x)
# compute_f_value(train_x, train_y)