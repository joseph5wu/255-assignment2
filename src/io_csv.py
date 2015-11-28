__author__ = 'joseph'

import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# ----- reading countries file into countries_data -----
COUNTRIES_COUNTRY_DESTINATION = 0
COUNTRIES_LAT_DESTINATION = 1
COUNTRIES_LNG_DESTINATION = 2
COUNTRIES_DISTANCE_KN = 3
COUNTRIES_DESTINATION_KM2 = 4
COUNTRIES_DESTINATION_LAN = 5
COUNTRIES_DESTINATION_LEVENSHTEIN_DISTANCE = 6

countries_data = []
def get_countries_data():
    with open('../data/countries.csv', 'rb') as countries_file:
        reader = csv.reader(countries_file)
        counts = 0
        for row in reader:
            counts += 1
            if counts == 1:
                continue
            countries_data.append(row)

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

users_data = []
def get_users_data():
    with open('../data/train_users.csv', 'rb') as users_file:
        reader = csv.reader(users_file)
        counts = 0
        for row in reader:
            counts += 1
            if counts == 1:
                continue
            users_data.append(row)


def analyze_users_data(users_data):
    destinations_data = defaultdict(int)
    countries_index = []
    countries_count = []
    index = 0
    genders_count = defaultdict(lambda: defaultdict(int))
    genders_index = set()

    age_data = defaultdict(lambda: defaultdict(int))

    for user in users_data:
        destination = user[USERS_COUNTRY_DESTINATION]
        gender = user[USERS_GENDER]

        age = user[USERS_AGE]
        if age == None or age == '':
            age = -1
        else:
            age = int(float(age))
        signup_method, signup_flow = user[USERS_SIGNUP_METHOD], user[USERS_SIGNUP_FLOW]
        # if destination == 'NDF':
        #     continue

        # count destination
        if destination not in destinations_data:
            destinations_data[destination] = index
            countries_index.append(destination)
            countries_count.append(1)
            index += 1
        else:
            destination_index = destinations_data[destination]
            countries_count[destination_index] += 1

        # count gender
        genders_index.add(gender)
        if destination not in genders_count:
            gender_count = defaultdict(int)
            gender_count.setdefault(gender, 1)
            genders_count.setdefault(destination, gender_count)
        else:
            gender_count = genders_count.get(destination)
            if gender not in gender_count:
                gender_count.setdefault(gender, 1)
            else:
                gender_count[gender] += 1

        # count age
        age_range = get_age_range(age)
        if destination not in age_data:
            age_dict = defaultdict(int)
            age_dict.setdefault(age_range, 1)
            age_data.setdefault(destination, age_dict)
        else:
            age_dict = age_data.get(destination)
            if age_range not in age_dict:
                age_dict.setdefault(age_range, 1)
            else:
                age_dict[age_range] += 1


    # draw destination and #users figure
    # analyze_general_users_data(countries_count, countries_index)
    # # draw destination and gender figure
    # analyze_gender_users_data(genders_index, genders_count, countries_index)
    # draw destination and age figure

    # analyze_age_users_data(users_data, countries_index, destinations_data)

    ## draw destination and account create date figure
    analyze_account_date_user_data(users_data, countries_index)

    # analyze_age_users_data(age_data, countries_index)
    analyze_age_users_data_in_some_ranges(age_data, countries_index, countries_count)



def analyze_general_users_data(countries_count, countries_index):
    plt.cla()
    rects = plt.bar(range(len(countries_count)), countries_count, align='center')
    auto_label(rects)
    plt.xticks(range(len(countries_index)), countries_index, size='small')
    plt.xlabel('Destination')
    plt.ylabel('#users')
    plt.title('Destination and #users in training data')

    # plt.show()
    plt.savefig('../images/destination_users.png')


def analyze_gender_users_data(genders_index, genders_count, countries_index):
    plt.cla()
    colors_set = ['r', 'y', 'g', 'b']
    index = 0
    width = 0.25
    gender_types = []
    gender_data = []
    for gender in genders_index:
        genders_count_list = []
        for destination in countries_index:
            if destination == 'NDF':
                continue
            count = genders_count.get(destination).get(gender)
            if count == None:
                count = 0
            genders_count_list.append(count)
        # print(gender, genders_count_list)
        rects = plt.bar([x + index * width for x in range(len(genders_count_list))],
                        genders_count_list, width, color=colors_set[index])
        index += 1
        gender_data.append(rects[0])
        gender_types.append(gender)
        # auto_label(rects)
    plt.xticks([x + 0.5 for x in range(len(countries_index) - 1)], countries_index[1:], size='small')
    plt.legend(gender_data, gender_types)
    plt.xlabel('Destination')
    plt.ylabel('#users of gender')
    plt.title('Destination and #users of gender in training data')

    # plt.show()
    plt.savefig('../images/destination_users_of_gender.png')


def get_age_range(age):
    if age < 0:
        return -1
    elif age >= 100:
        return 10
    else:
        return age / 10

def get_age_range_desc(age_range):
    if age_range == -1:
        return '-unknown-'
    elif age_range == 10:
        return '>=100'
    else:
        return str(age_range * 10) + '-' + str(age_range * 10 + 9)


def get_age_range_list():
    return range(-1, 11)


def analyze_age_users_data(age_data, countries_index, countries_count):
    plt.cla()
    colors = ['r', 'k', 'b', 'g', 'c', 'm', 'y', 'b', 'k', 'k', 'k', 'r']
    index = 0
    width = 0.08
    age_ranges = []
    age_rects_data = []
    age_range_list = get_age_range_list()
    for age_range in age_range_list:
        age_count_list = []
        for i in range(len(countries_index)):
            destination = countries_index[i]
            if destination == 'NDF':
                continue
            count = age_data.get(destination).get(age_range)
            if count == None:
                count = 0

            age_count_list.append(float(count) / countries_count[i])

        rects = plt.bar([x + index * width for x in range(len(age_count_list))],
                        age_count_list, width, color=colors[index])
        index += 1
        age_rects_data.append(rects[0])
        age_ranges.append(get_age_range_desc(age_range))

    plt.xticks([x + 0.5 for x in range(len(countries_index) - 1)], countries_index[1:], size='small')
    plt.legend(age_rects_data, age_ranges)
    plt.xlabel('Destination')
    plt.ylabel('#users of age')
    plt.title('Destination and #users of age in training data')
    # plt.show()
    plt.savefig('../images/destination_users_of_age.png')


def analyze_age_users_data_in_some_ranges(age_data, countries_index, countries_count):
    age_list = [2, 3, 4, 5]
    for age_range in age_list:
        plt.cla()
        age_count_list = []
        for i in range(len(countries_index)):
            destination = countries_index[i]
            if destination == 'NDF':
                continue
            count = age_data.get(destination).get(age_range)
            if count == None:
                count = 0
            age_count_list.append(float(count) / countries_count[i])

        rects = plt.bar(range(len(age_count_list)), age_count_list, 0.5, color='b')
        # auto_label_float(rects)

        plt.xticks([x + 0.5 for x in range(len(countries_index) - 1)], countries_index[1:], size='small')
        plt.xlabel('Destination')
        plt.ylabel('#users of age')
        plt.title('Destination and #users of age(' + get_age_range_desc(age_range) + ') in training data')
        # plt.show()
        plt.savefig('../images/destination_users_of_age(' + get_age_range_desc(age_range) + ').png')


def analyze_account_date_user_data(users_data, countries_index):
    color_set = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    year = 2010
    destination_account_date = defaultdict(lambda: defaultdict(int))
    for destinations in countries_index:
        local = defaultdict(int)
        for i in range(1, 13):
            local.setdefault(i, 0)
        destination_account_date.setdefault(destinations, local)

    for user in users_data:
        destination = user[USERS_COUNTRY_DESTINATION]
        account_date = user[USERS_DATE_ACCOUNT_CREATED].split('-')
        if account_date[0] == '2013':
            month = int(account_date[1])
            destination_account_date[destination][month] += 1

    rects_data = []
    for i in range(1, 13):
        country_month_list = []
        for k in countries_index:
            country_month_list.append(destination_account_date[k][i])
        print country_month_list
        width = 1.0 / 13
        rects = plt.bar([x + (i - 1) * width for x in range(len(countries_index))], country_month_list, width, color = color_set[i % 7])
        rects_data.append(rects[0])
    plt.xticks([x + 0.5 for x in range(len(countries_index))], countries_index[0:], size='small')
    #plt.show()
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    plt.legend(rects_data, month_list)
    plt.xlabel('Destination')
    plt.ylabel('#number of users')
    plt.title('Destination and #users of month in training data 2013')
    plt.savefig('../images/destination_users_of_month_2013.png')


def auto_label(rects):
   for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 5., 1.03 * height, '%d' % int(height),
                 ha='center', va='bottom')


def auto_label_float(rects):
   for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 5., 1.03 * height, '%f' % round(float(height), 3),
                 ha='center', va='bottom')

get_users_data()
analyze_users_data(users_data)

# for i in range(len(countries_index)):
#     country = countries_index[i]
#     country_data = destinations_data.get(country)
#     plt.plot(i, country_data)

# destinations = []
# destinations_name = []
# destinations_index = defaultdict(int)
# index = 0
# for user in users_data:
#     destination = user[USERS_COUNTRY_DESTINATION]
#     if destination == 'NDF':
#         continue
#     if destination not in destinations_index:
#         destinations_index.setdefault(destination, index)
#         destinations_name.append(destination)
#         index += 1
#     destination_index = destinations_index.get(destination)
#     destinations.append(destination_index)
# plt.hist(destinations)
# plt.xticks(range(len(destinations_name)), destinations_name)
# plt.show()

# ----- reading age_gender_bkts file into age/gender data -----
BKTS_AGE_BUCKET = 0
BKTS_COUNTRY_DESTINATION = 1
BKTS_GENDER = 2
BKTS_POPULATION_IN_THOUSANDS = 3
BKTS_YEAR = 4

age_bkts_data = defaultdict(lambda: defaultdict(lambda: defaultdict))
gender_bkts_data = defaultdict(lambda: defaultdict(lambda: defaultdict))
def get_bkts_data():
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

# ----- reading session file into session_data -----
SESSION_USER_ID = 0
SESSION_ACTION = 1
SESSION_ACTION_TYPE = 2
SESSION_DETAIL = 3
SESSION_DEVICE_TYPE = 4
SESSION_SECS_ELAPSED = 5
session_data = defaultdict(lambda: defaultdict(float))
def get_session_data():
    with open('../data/sessions.csv', 'rb') as session_file:
        reader = csv.reader(session_file)
        counts = 0
        for row in reader:
            counts += 1
            if counts == 1:
                continue

            userId, action, detail = row[SESSION_USER_ID], row[SESSION_ACTION], row[SESSION_DETAIL]
            if row[SESSION_SECS_ELAPSED] and row[SESSION_SECS_ELAPSED] != '':
                secs = float(row[SESSION_SECS_ELAPSED])
            else:
                secs = 0
            if detail and detail != '' and detail != '-unknown-':
                action = detail

            if userId not in session_data:
                action_dict = defaultdict(float)
                action_dict.setdefault(action, secs)
                session_data.setdefault(userId, action_dict)
            else:
                action_dict = session_data.get(userId)
                if action not in action_dict:
                    action_dict.setdefault(action, secs)
                else:
                    action_dict[action] += secs
