import csv
import os


def return_csv(file_path):
    cur_path = os.path.dirname(__file__)
    file = os.path.relpath(file_path, cur_path)
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append(dict(row))
        if len(result) == 1:
            return result[0]
        else:
            return result

file_path = 'spec/3_month_avg/Site-Stats-Over-Time-Jun-01-2018-Aug-31-2018-byMonth-thespec-com.csv'

print(return_csv(file_path))