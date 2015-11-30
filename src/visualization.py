__author__ = 'joseph'

import pandas as pd
from vincent import *
from collections import defaultdict
import load_data as load


def increase_data(key, destination, data):
    if key not in data:
        destination_dict = defaultdict(int)
        destination_dict.setdefault(destination, 1)
        data.setdefault(key, destination_dict)
    else:
        destination_dict = data.get(key)
        if destination not in destination_dict:
            destination_dict.setdefault(destination, 1)
        else:
            destination_dict[destination] += 1


# compare month
users_data, users_dict = load.get_train_users_data()
month_data = defaultdict(lambda: defaultdict(int))
book_month_data = defaultdict(lambda: defaultdict(int))
gender_data = defaultdict(lambda: defaultdict(int))
age_data = defaultdict(lambda: defaultdict(int))
language_data = defaultdict(lambda: defaultdict(int))
affiliate_provider_data = defaultdict(lambda: defaultdict(int))
first_device_type_data = defaultdict(lambda: defaultdict(int))
first_browser_data = defaultdict(lambda: defaultdict(int))

for user in users_data:
    destination = user[load.USERS_COUNTRY_DESTINATION]

    timestamp_first_active = user[load.USERS_TIMESTAMP_FIRST_ACTIVE]
    year = int(timestamp_first_active[:4])
    month = int(timestamp_first_active[4:6])
    day = int(timestamp_first_active[6:8])

    if destination != 'NDF':
        date_first_booking = user[load.USERS_DATE_FIRST_BOOKING].strip().split('-')
        book_year = int(date_first_booking[0])
        book_month = int(date_first_booking[1])
        book_day = int(date_first_booking[2])
        increase_data(book_month, destination, book_month_data)

    gender = user[load.USERS_GENDER]
    age = user[load.USERS_AGE]
    if age is None or age == '':
        age = '-unknown-'
    else:
        age = str(int(age) / 10) + '-' + str(int(age) / 10 + 9)

    language = user[load.USERS_LANGUAGE]
    affiliate_provider = user[load.USERS_AFFILIATE_PROVIDER]
    first_device_type = user[load.USERS_FIRST_DEVICE_TYPE]
    first_browser = user[load.USERS_FIRST_BROWSER]

    increase_data(month, destination, month_data)
    increase_data(gender, destination, gender_data)
    increase_data(age, destination, age_data)
    increase_data(language, destination, language_data)
    increase_data(affiliate_provider, destination, affiliate_provider_data)
    increase_data(first_device_type, destination, first_device_type_data)
    increase_data(first_browser, destination, first_browser_data)


def visualization(data, is_large, x_desc, y_desc, title):
    index = []
    value = []
    key_list = data.keys()
    key_list.sort()
    for key in key_list:
        index.append(key)
        datum = data.get(key)
        if is_large:
            value.append({'NDF': datum['NDF'], 'US': datum['US'], 'other': datum['other']})
        else:
            value.append({'AU': datum['AU'], 'CA': datum['CA'], 'DE': datum['DE'],
                          'ES': datum['ES'], 'FR': datum['FR'], 'GB': datum['GB'],
                          'IT': datum['IT'], 'NL': datum['NL'], 'PT': datum['PT']})

    df = pd.DataFrame(value, index=index)
    vis = GroupedBar(df)
    vis.axis_titles(x=x_desc, y=y_desc)
    vis.width = 1000
    vis.legend(title=title)
    vis.colors(brew='Pastel1')
    vis.display()



