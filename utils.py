import csv
import os
# from pprint import pprint
from decimal import Decimal, ROUND_UP
import re


def process_csv(file_path, report_type, site):
    # get list of dicts representing rows in CSV file
    stats_all = return_csv(file_path)
    stats_ref = stats_all[1:]
    stats_target = stats_all[0]
    units = len(stats_ref)
    stats = {}
    stats['site_stats'] = site_stats(stats_target, stats_ref, units)
    stats['report'] = report_type
    stats['unit'] = report_type.replace('ly', '').replace('dai', 'day')
    stats['ma'] = f"{str(units)} {stats['unit']}s"
    stats['site'] = site
    return stats


def site_stats(new, ma, units):
    result = {
        "date": new['Date'],
        'posts': {
            "new": new['New Posts'],
            "ma": get_avg_values(ma, 'New Posts'),
            "kpi_delta": '',
        },
        "pagev": {
            "new": new['Views (all pages)'],
            "total": sum_csv_values(ma, 'Views (all pages)'),
            "avg": get_avg_values(ma, 'Views (all pages)'),
            "delta": '',
            'kpi_new': '',
            'kpi_ma': '',
            'kpi_delta': '',
        },
        "postv": {
            "new": new['Views (posts)'],
            "total": sum_csv_values(ma, 'Views (posts)'),
            "avg": get_avg_values(ma, 'Views (posts)'),
            "delta": '',
            'kpi_new': '',
            'kpi_ma': '',
            'kpi_delta': '',
        },
        "visitors": {
            "new": new['Visitors (posts)'],
            "new_pages": new['Visitors (all pages)'],
            "avg_pages": get_avg_values(ma, 'Visitors (all pages)'),
            "total_pages": sum_csv_values(ma, 'Visitors (all pages)'),
            "total": sum_csv_values(ma, 'Visitors (posts)'),
            "avg": get_avg_values(ma, 'Visitors (posts)'),
            "delta": '',
        },
        "minutes": {
            "new": new['Engaged Minutes (posts)'],
            "new_pages": new['Engaged Minutes (all pages)'],
            "avg_pages": get_avg_values(ma, 'Engaged Minutes (all pages)'),
            "total_pages": sum_csv_values(ma, 'Engaged Minutes (all pages)'),
            "total": sum_csv_values(ma, 'Engaged Minutes (posts)'),
            "avg": get_avg_values(ma, 'Engaged Minutes (posts)'),
            "delta": '',
            "kpi_new": '',
            'kpi_new_ma': '',
            'kpi_new_ma_delta': '',
            "kpi_pages": '',
            "kpi_pages_ma": '',
            "kpi_pages_ma_delta": '',
        },
        "visitor_type": {
            "new": percentage(new['New vis.'], new['Visitors (posts)']),
            "new_ma%": percentage(sum_csv_values(ma, 'New vis.'), sum_csv_values(ma, 'Visitors (posts)')),
            "returning": percentage(new['Returning vis.'], new['Visitors (posts)']),
            "returning_ma%": percentage(sum_csv_values(ma, 'Returning vis.'), sum_csv_values(ma, 'Visitors (posts)')),
        },
        "devices": {
            "mobile": new['Mobile views'],
            "mobile_ma%": percentage(sum_csv_values(ma, 'Mobile views'), sum_csv_values(ma, 'Views (posts)')),
            "desktop": new['Desktop views'],
            "desktop_ma%": percentage(sum_csv_values(ma, 'Desktop views'), sum_csv_values(ma, 'Views (posts)')),
            "tablet": new['Tablet views'],
            "tablet_ma%": percentage(sum_csv_values(ma, 'Tablet views'), sum_csv_values(ma, 'Views (posts)'))
        },
        "traffic": {
            "search": new['Search refs'],
            "search%": '',
            "search_ma": sum_csv_values(ma, 'Search refs'),
            "search_ma%": '',
            'search_pv_ma%': vs_ma(new['Search refs'], get_avg_values(ma, 'Search refs')),
            'search_pv_diff': '',
            "other": new['Other refs'],
            "other%": '',
            "other_ma": sum_csv_values(ma, 'Other refs'),
            "other_ma%": '',
            'other_pv_ma%': vs_ma(new['Other refs'], get_avg_values(ma, 'Other refs')),
            'other_pv_diff': '',
            "internal": new['Internal refs'],
            "internal%": '',
            "internal_ma": sum_csv_values(ma, 'Internal refs'),
            "internal_ma%": '',
            'internal_pv_ma%': vs_ma(new['Internal refs'], get_avg_values(ma, 'Internal refs')),
            'internal_pv_diff': '',
            "direct": new['Direct refs'],
            "direct%": '',
            "direct_ma": sum_csv_values(ma, 'Direct refs'),
            "direct_ma%": '',
            'direct_pv_ma%': vs_ma(new['Direct refs'], get_avg_values(ma, 'Direct refs')),
            'direct_pv_diff': '',
            "fb": new['Fb refs'],
            "fb%": '',
            "fb_ma": sum_csv_values(ma, 'Fb refs'),
            "fb_ma%": '',
            'fb_pv_diff': '',
            'fb_pv_ma%': vs_ma(new['Fb refs'], get_avg_values(ma, 'Fb refs')),
            "tco": new['Tw refs'],
            "tco%": '',
            "tco_ma": sum_csv_values(ma, 'Tw refs'),
            "tco_ma%": '',
            'tco_pv_ma%': vs_ma(new['Tw refs'], get_avg_values(ma, 'Tw refs')),
            'tco_pv_diff': ''
        }
    }
    result['pagev']['delta'] = vs_ma(result['pagev']['new'], result['pagev']['avg'])
    result['postv']['delta'] = vs_ma(result['postv']['new'], result['postv']['avg'])
    result['visitors']['delta'] = vs_ma(result['visitors']['new'], result['visitors']['avg'])
    result['visitors']['total_delta'] = vs_ma(result['visitors']['new_pages'], result['visitors']['avg_pages'])
    result['minutes']['delta'] = vs_ma(result['minutes']['new'], result['minutes']['avg'])
    result['minutes']['total_delta'] = vs_ma(result['minutes']['new_pages'], result['minutes']['avg_pages'])
    result['devices']['mobile%'] = percentage(result['devices']['mobile'], result['postv']['new'])
    result['devices']['desktop%'] = percentage(result['devices']['desktop'], result['postv']['new'])
    result['devices']['tablet%'] = percentage(result['devices']['tablet'], result['postv']['new'])
    result['postv']['kpi_new'] = str(round((float(result['postv']['new']) / float(result['visitors']['new'])), 2))
    result['postv']['kpi_ma'] = str(round((float(result['postv']['total']) / float(result['visitors']['total'])), 2))
    result['postv']['kpi_delta'] = vs_ma(result['postv']['kpi_new'], result['postv']['kpi_ma'])
    result['pagev']['kpi_new'] = str(round((float(result['pagev']['new']) / float(result['visitors']['new_pages'])), 2))
    result['pagev']['kpi_ma'] = str(round((float(result['pagev']['total']) / float(result['visitors']['total_pages'])), 2))
    result['pagev']['kpi_delta'] = vs_ma(result['pagev']['kpi_new'], result['pagev']['kpi_ma'])
    result['minutes']['kpi_pages'] = str(round((float(result['minutes']['new_pages']) / float(result['visitors']['new_pages'])), 2))
    result['minutes']['kpi_pages_ma'] = str(round((float(result['minutes']['total_pages']) / float(result['visitors']['total_pages'])), 2))
    result['minutes']['kpi_pages_ma_delta'] = vs_ma( result['minutes']['kpi_pages'], result['minutes']['kpi_pages_ma'])
    result['minutes']['kpi_new'] = str(round((float(result['minutes']['new']) / float(result['visitors']['new'])), 2))
    result['minutes']['kpi_new_ma'] = str(round((float(result['minutes']['total']) / float(result['visitors']['total'])), 2))
    result['minutes']['kpi_new_ma_delta'] = vs_ma(result['minutes']['kpi_new'], result['minutes']['kpi_new_ma']) 
    result['traffic']['search%'] = percentage(result['traffic']['search'], result['postv']['new'])
    result['traffic']['other%'] = percentage(result['traffic']['other'], result['postv']['new'])
    result['traffic']['internal%'] = percentage(result['traffic']['internal'], result['postv']['new'])
    result['traffic']['direct%'] = percentage(result['traffic']['direct'], result['postv']['new'])
    result['traffic']['fb%'] = percentage(result['traffic']['fb'], result['postv']['new'])
    result['traffic']['tco%'] = percentage(result['traffic']['tco'], result['postv']['new'])
    result['traffic']['search_ma%'] = percentage(result['traffic']['search_ma'], result['postv']['total'])
    result['traffic']['other_ma%'] = percentage(result['traffic']['other_ma'], result['postv']['total'])
    result['traffic']['internal_ma%'] = percentage(result['traffic']['internal_ma'], result['postv']['total'])
    result['traffic']['direct_ma%'] = percentage(result['traffic']['direct_ma'], result['postv']['total'])
    result['traffic']['fb_ma%'] = percentage(result['traffic']['fb_ma'], result['postv']['total'])
    result['traffic']['tco_ma%'] = percentage(result['traffic']['tco_ma'], result['postv']['total'])
    result['traffic']['fb_pv_diff'] = humanize_number(float(new['Fb refs']) - float(get_avg_values(ma, 'Fb refs')), 1)
    result['traffic']['tco_pv_diff'] = humanize_number(float(new['Tw refs']) - float(get_avg_values(ma, 'Tw refs')), 1)
    result['traffic']['direct_pv_diff'] = humanize_number(float(new['Direct refs']) - float(get_avg_values(ma, 'Direct refs')), 1)
    result['traffic']['internal_pv_diff'] = humanize_number(float(new['Internal refs']) - float(get_avg_values(ma, 'Internal refs')), 1)
    result['traffic']['other_pv_diff'] = humanize_number(float(new['Other refs']) - float(get_avg_values(ma, 'Other refs')), 1)
    result['traffic']['search_pv_diff'] = humanize_number(float(new['Search refs']) - float(get_avg_values(ma, 'Search refs')), 1)
    result['posts']['kpi_delta'] = vs_ma(result['posts']['new'], result['posts']['ma'])
    return result


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


def newest(folder):
    cur_path = os.path.dirname(__file__)
    folder_path = os.path.relpath(folder, cur_path)
    files = os.listdir(folder_path)
    paths = [os.path.join(folder_path, basename) for basename in files if basename.endswith('.csv')]
    return max(paths, key=os.path.getctime)


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


def sum_csv_values(d, key):
    # get and sum values from CSV (converted to dict) given a key
    # divisor = len(d)
    # print("Divisor is: ", divisor)
    # assume all values are string represenations of integers, though some end in '.0'
    # values that are string reps of floats we aren't dealing with at moment
    result = [int(item[key].replace('.0', '')) for item in d]
    theSum = sum(result)
    return str(theSum)


def sum_safe(l):
    #  handles if item is no value in list
    new_list = []
    for item in l:
        if not item:
            item = '0'
        item = float(item)
        new_list.append(item)
    return sum(new_list)


def humanize_number(value, fraction_point=1):
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
