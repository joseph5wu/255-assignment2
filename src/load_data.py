__author__ = 'joseph'

import csv
from collections import defaultdict

# ----- reading countries file into countries_data -----
COUNTRIES_COUNTRY_DESTINATION = 0
COUNTRIES_LAT_DESTINATION = 1
COUNTRIES_LNG_DESTINATION = 2
COUNTRIES_DISTANCE_KM = 3
COUNTRIES_DESTINATION_KM2 = 4
COUNTRIES_DESTINATION_LAN = 5
COUNTRIES_DESTINATION_LEVENSHTEIN_DISTANCE = 6


# ----- reading countries file into countries_data -----
def get_countries_data():
    countries_data = []
    countries_dict = defaultdict(list)
    with open('../data/countries.csv', 'rb') as countries_file:
        reader = csv.reader(countries_file)
        counts = 0
        for row in reader:
            counts += 1
            if counts == 1:
                continue
            countries_data.append(row)
            countries_dict.setdefault(row[COUNTRIES_COUNTRY_DESTINATION], row)

    return countries_data, countries_dict

# ----- reading train_users file into countries_data -----
USERS_ID = 0
USERS_DATE_ACCOUNT_CREATED = 1
USERS_TIMESTAMP_FIRST_ACTIVE = 2
USERS_DATE_FIRST_BOOKING = 3
USERS_GENDER = 4
USERS_AGE = 5
USERS_SIGNUP_METHOD = 6
USERS_SIGNUP_FLOW = 7
USERS_LANGUAGE = 8
USERS_AFFILIATE_CHANNEL = 9
USERS_AFFILIATE_PROVIDER = 10
USERS_FIRST_AFFILIATE_TRACKED = 11
USERS_SIGNUP_APP = 12
USERS_FIRST_DEVICE_TYPE = 13
USERS_FIRST_BROWSER = 14
USERS_COUNTRY_DESTINATION = 15


def get_users_data(file_name):
    users_data = []
    users_dict = defaultdict(list)
    with open(file_name, 'rb') as users_file:
        reader = csv.reader(users_file)
        counts = 0
        for row in reader:
            counts += 1
            if counts == 1:
                continue
            users_data.append(row)
            users_dict.setdefault(row[USERS_ID], row)

    return users_data, users_dict


def get_train_users_data():
    return get_users_data('../data/train_users.csv')


def get_test_users_data():
    return get_users_data('../data/test_users.csv')

# ----- reading age_gender_bkts file into age/gender data -----
BKTS_AGE_BUCKET = 0
BKTS_COUNTRY_DESTINATION = 1
BKTS_GENDER = 2
BKTS_POPULATION_IN_THOUSANDS = 3
BKTS_YEAR = 4


def get_bkts_data():
    age_bkts_data = defaultdict(lambda: defaultdict(lambda: defaultdict))
    gender_bkts_data = defaultdict(lambda: defaultdict(lambda: defaultdict))
    with open('../data/age_gender_bkts.csv', 'rb') as age_gender_file:
        reader = csv.reader(age_gender_file)
        counts = 0
        for row in reader:
            counts += 1
            if counts == 1:
                continue

            age, destination, gender = row[BKTS_AGE_BUCKET], row[BKTS_COUNTRY_DESTINATION], row[BKTS_GENDER]
            population = float(row[BKTS_POPULATION_IN_THOUSANDS])
            # insert record into dict(age, dict(country, dict(gender, population)))
            if age not in age_bkts_data:
                gender_set = defaultdict(int)
                gender_set.setdefault(gender, population)
                country_dict = defaultdict(lambda: defaultdict)
                country_dict.setdefault(destination, gender_set)
                age_bkts_data.setdefault(age, country_dict)
            else:
                country_dict = age_bkts_data.get(age)
                if destination not in country_dict:
                    gender_set = defaultdict(int)
                    gender_set.setdefault(gender, population)
                    country_dict.setdefault(destination, gender_set)
                else:
                    gender_set = country_dict.get(destination)
                    gender_set.setdefault(gender, population)

            # insert record into dict(gender, dict(country, dict(age, population)))
            if gender not in gender_bkts_data:
                age_set = defaultdict(int)
                age_set.setdefault(age, population)
                country_dict = defaultdict(lambda: defaultdict)
                country_dict.setdefault(destination, age_set)
                gender_bkts_data.setdefault(gender, country_dict)
            else:
                country_dict = gender_bkts_data.get(gender)
                if destination not in country_dict:
                    age_set = defaultdict(int)
                    age_set.setdefault(age, population)
                    country_dict.setdefault(destination, age_set)
                else:
                    age_set = country_dict.get(destination)
                    age_set.setdefault(age, population)

    return age_bkts_data, gender_bkts_data

# ----- reading session file into session_data -----
SESSION_USER_ID = 0
SESSION_ACTION = 1
SESSION_ACTION_TYPE = 2
SESSION_DETAIL = 3
SESSION_DEVICE_TYPE = 4
SESSION_SECS_ELAPSED = 5


def get_session_data():
    session_data = defaultdict(float)
    total_time = 0
    users_count = 0
    prev_user_id = None
    with open('../data/sessions.csv', 'rb') as session_file:
        reader = csv.reader(session_file)
        counts = 0
        for row in reader:
            counts += 1
            if counts == 1:
                continue

            user_id, action, detail = row[SESSION_USER_ID], row[SESSION_ACTION], row[SESSION_DETAIL]
            if detail and detail != '' and detail != '-unknown-':
                action = detail

            if action != 'view_search_results':
                continue

            if prev_user_id is None:
                prev_user_id = user_id
            if prev_user_id != user_id:
                users_count += 1
                prev_user_id = user_id

            if row[SESSION_SECS_ELAPSED] and row[SESSION_SECS_ELAPSED] != '':
                secs = float(row[SESSION_SECS_ELAPSED])
            else:
                secs = 0

            if user_id not in session_data:
                session_data.setdefault(user_id, secs)
            else:
                session_data[user_id] += secs
            total_time += secs
    return session_data, total_time, users_count
