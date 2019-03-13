# from pprint import pprint
from decimal import Decimal, ROUND_UP
import re


def vs_ma(new, avg):
    # print("New value: ", humanize_number(new))
    # print("Avg value: ", humanize_number(daily_avg, 0))
    result = ((float(new) - float(avg)) / float(avg)) * 100
    result = f"{str(round(result, 1))}"
    return result


def get_avg_values(the_list, key):
    # get avg values of specific key in list of dicts
    # print("Divisor is: ", divisor)
    # assume all values are string represenations of integers, though some end in '.0'
    # assume no empty values
    # values that are string reps of floats we aren't dealing with at moment
    result = [int(item[key].replace('.0', '')) for item in the_list]
    the_average = sum(result) / len(result)
    return str(Decimal(the_average).quantize(Decimal('1.'), rounding=ROUND_UP))


def sum_safe(l):
    #  handles if item is no value in list
    new_list = []
    for item in l:
        if not item:
            item = '0'
        item = float(item)
        new_list.append(item)
    return sum(new_list)


def humanize(value, fraction_point=1):
    if value is not '':
        powers = [10 ** x for x in (12, 9, 6, 3, 0)]
        human_powers = ('T', 'B', 'M', 'K', '')
        is_negative = False
        if not isinstance(value, float):
            value = float(value)
        if value < 0:
            is_negative = True
            value = abs(value)
        for i, p in enumerate(powers):
            if value >= p:
                return_value = str(round(value / (p / (10.0 ** fraction_point))) /
                                  (10 ** fraction_point)) + human_powers[i]
                break
        if is_negative:
            return_value = "-" + return_value
        # remove pesky situation where xXX.0 occurs
        # return_value = return_value.replace('.0', '')
        return_value = re.sub(r'.0$', '', return_value)
        return return_value.replace('.0K', 'K')
    else:
        return '0'


def percentage(part, total):
    # have to take into account part might be none (actually '')
    if part is not '':
        result = str(round((float(part) / float(total)) * 100, 0)).replace('.0', '')
        return result
    else:
        return '0'
