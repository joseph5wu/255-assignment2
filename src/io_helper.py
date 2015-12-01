__author__ = 'joseph'

import csv


def write_map_data(data_map, file_name):
    with open(file_name, 'wb') as output_file:
        writer = csv.writer(output_file)
        for key in data_map:
            value = data_map[key]
            writer.writerow([key, value])


def read_map_data(file_name):
    data_map = {}
    with open(file_name, 'rb') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            data_map.setdefault(int(row[0]), row[1])

    return data_map
