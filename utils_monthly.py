import csv
import os


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
    divisor = len(d)
    # print("Divisor is: ", divisor)
    # assume all values are string represenations of integers, though some end in '.0'
    # values that are string reps of floats we aren't dealing with at moment
    result = [int(item[key].replace('.0', '')) for item in d]
    theSum = sum(result)
    return str(theSum)


def vs_ma(new, avg, days):
    daily_avg = float(avg)/days
    # print("New value: ", humanize_number(new))
    # print("Avg value: ", humanize_number(daily_avg, 0))
    result = ((float(new) - daily_avg)/daily_avg)*100
    result = f"{str(round(result, 1))}"
    return result


def humanize_number(value, fraction_point=1):
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
    return_value = return_value.replace('.0', '')
    return return_value


def percentage(part, total):
    result = str(round((float(part)/float(total)) * 100, 0)).replace('.0', '')
    return result


def site_stats(new, ma, units):
    result = {
        "pagev": {
            "new": new['Views (all pages)'],
            "avg": sum_csv_values(ma, 'Views (all pages)'),
            "delta": ''
        },
        "postv": {
            "new": new['Views (posts)'],
            "avg": sum_csv_values(ma, 'Views (posts)'),
            "delta": '',
            "kpi_new": '',
        },
        "visitors": {
            "new": new['Visitors (posts)'],
            "avg": sum_csv_values(ma, 'Visitors (posts)'),
            "delta": '',
        },
        "minutes": {
            "new": new['Engaged Minutes (posts)'],
            "avg": sum_csv_values(ma, 'Engaged Minutes (posts)'),
            "delta": '',
            "kpi_new": '',
        },
        "visitor_type": {
            "new": percentage(new['New vis.'], new['Visitors (posts)']),
            "returning": percentage(new['Returning vis.'], new['Visitors (posts)'])
        },
        "devices": {
            "mobile": new['Mobile views'],
            "desktop": new['Desktop views'],
            "tablet": new['Tablet views']
        },
        "traffic": {
            "s+o": str(float(new['Search refs']) + float(new['Other refs'])),
            "internal": new['Internal refs'],
            "direct": new['Direct refs'],
            "fb": new['Fb refs'],
            "tco": new['Tw refs']
        }
    }

    result['pagev']['delta'] = vs_ma(result['pagev']['new'], result['pagev']['avg'], units)
    result['postv']['delta'] = vs_ma(result['postv']['new'], result['postv']['avg'], units)
    result['visitors']['delta'] = vs_ma(result['visitors']['new'], result['visitors']['avg'], units)
    result['minutes']['delta'] = vs_ma(result['minutes']['new'], result['minutes']['avg'], units)
    result['devices']['mobile'] = percentage(result['devices']['mobile'], result['postv']['new'])
    result['devices']['desktop'] = percentage(result['devices']['desktop'], result['postv']['new'])
    result['devices']['tablet'] = percentage(result['devices']['tablet'], result['postv']['new'])
    result['postv']['kpi_new'] = str(round((float(result['postv']['new'])/float(result['visitors']['new'])), 2))
    result['minutes']['kpi_new'] = str(round((float(result['minutes']['new'])/float(result['visitors']['new'])), 2))
    return result
