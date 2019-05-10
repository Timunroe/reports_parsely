# internal
import json
from datetime import datetime
import calendar
import statistics
# 3rd party
from bottle import template
# mine
from utils import utils_io

'''
find content by day, then time
{
    'monday': {
        '0': {'pv': 1234, 'uv': 2345', 'articles': 123},
        '1': {'pv': 2345, 'uv': 3456', 'articles': 243}
    },
    'tuesday': {
        '0': {'pv': 1234, 'uv': 2345', 'articles': 123},
        '1': {'pv': 2345, 'uv': 3456', 'articles': 243}
    }
'''

final_data = {'Monday': {'12 AM': {'PV': 1047, 'UV': 536}, '1 AM': {'PV': 645, 'UV': 358}, '2 AM': {'PV': 504, 'UV': 265}, '3 AM': {'PV': 506, 'UV': 268}, '4 AM': {'PV': 553, 'UV': 256}, '5 AM': {'PV': 1221, 'UV': 510}, '6 AM': {'PV': 3356, 'UV': 1169}, '7 AM': {'PV': 5110, 'UV': 1851}, '8 AM': {'PV': 6749, 'UV': 2444}, '9 AM': {'PV': 6758, 'UV': 2623}, '10 AM': {'PV': 5434, 'UV': 2340}, '11 AM': {'PV': 6213, 'UV': 2773}, '12 PM': {'PV': 6585, 'UV': 2771}, '1 PM': {'PV': 6244, 'UV': 2685}, '2 PM': {'PV': 5245, 'UV': 2475}, '3 PM': {'PV': 5624, 'UV': 2452}, '4 PM': {'PV': 4690, 'UV': 2226}, '5 PM': {'PV': 4581, 'UV': 2304}, '6 PM': {'PV': 4436, 'UV': 2183}, '7 PM': {'PV': 4032, 'UV': 2170}, '8 PM': {'PV': 4358, 'UV': 2256}, '9 PM': {'PV': 3931, 'UV': 2009}, '10 PM': {'PV': 2953, 'UV': 1657}, '11 PM': {'PV': 2100, 'UV': 1070}}, 'Tuesday': {'12 AM': {'PV': 2171, 'UV': 1301}, '1 AM': {'PV': 1727, 'UV': 996}, '2 AM': {'PV': 1281, 'UV': 739}, '3 AM': {'PV': 947, 'UV': 556}, '4 AM': {'PV': 1069, 'UV': 590}, '5 AM': {'PV': 1836, 'UV': 855}, '6 AM': {'PV': 4366, 'UV': 1727}, '7 AM': {'PV': 8148, 'UV': 2806}, '8 AM': {'PV': 11078, 'UV': 4111}, '9 AM': {'PV': 11200, 'UV': 4477}, '10 AM': {'PV': 9720, 'UV': 4283}, '11 AM': {'PV': 9870, 'UV': 4611}, '12 PM': {'PV': 9989, 'UV': 4562}, '1 PM': {'PV': 7940, 'UV': 3824}, '2 PM': {'PV': 7438, 'UV': 3610}, '3 PM': {'PV': 7696, 'UV': 3729}, '4 PM': {'PV': 7420, 'UV': 3743}, '5 PM': {'PV': 7615, 'UV': 3958}, '6 PM': {'PV': 7878, 'UV': 4084}, '7 PM': {'PV': 7436, 'UV': 3825}, '8 PM': {'PV': 7771, 'UV': 3766}, '9 PM': {'PV': 6773, 'UV': 3511}, '10 PM': {'PV': 5714, 'UV': 2907}, '11 PM': {'PV': 4004, 'UV': 2063}}, 'Wednesday': {'12 AM': {'PV': 1104, 'UV': 574}, '1 AM': {'PV': 740, 'UV': 412}, '2 AM': {'PV': 629, 'UV': 322}, '3 AM': {'PV': 509, 'UV': 285}, '4 AM': {'PV': 533, 'UV': 280}, '5 AM': {'PV': 1193, 'UV': 477}, '6 AM': {'PV': 3027, 'UV': 954}, '7 AM': {'PV': 5520, 'UV': 1644}, '8 AM': {'PV': 7069, 'UV': 2409}, '9 AM': {'PV': 7621, 'UV': 2671}, '10 AM': {'PV': 6828, 'UV': 2544}, '11 AM': {'PV': 6300, 'UV': 2626}, '12 PM': {'PV': 6513, 'UV': 2620}, '1 PM': {'PV': 5282, 'UV': 2236}, '2 PM': {'PV': 4871, 'UV': 2130}, '3 PM': {'PV': 4824, 'UV': 2068}, '4 PM': {'PV': 4342, 'UV': 2051}, '5 PM': {'PV': 4381, 'UV': 1985}, '6 PM': {'PV': 3898, 'UV': 1846}, '7 PM': {'PV': 3814, 'UV': 1792}, '8 PM': {'PV': 4097, 'UV': 1887}, '9 PM': {'PV': 3614, 'UV': 1694}, '10 PM': {'PV': 3184, 'UV': 1413}, '11 PM': {'PV': 1921, 'UV': 959}}, 'Thursday': {'12 AM': {'PV': 1418, 'UV': 661}, '1 AM': {'PV': 865, 'UV': 486}, '2 AM': {'PV': 706, 'UV': 355}, '3 AM': {'PV': 445, 'UV': 285}, '4 AM': {'PV': 625, 'UV': 326}, '5 AM': {'PV': 1319, 'UV': 535}, '6 AM': {'PV': 2770, 'UV': 1061}, '7 AM': {'PV': 4981, 'UV': 1862}, '8 AM': {'PV': 6974, 'UV': 2470}, '9 AM': {'PV': 7484, 'UV': 2865}, '10 AM': {'PV': 6460, 'UV': 2622}, '11 AM': {
    'PV': 6561, 'UV': 2971}, '12 PM': {'PV': 6497, 'UV': 2738}, '1 PM': {'PV': 4883, 'UV': 2346}, '2 PM': {'PV': 4926, 'UV': 2191}, '3 PM': {'PV': 5411, 'UV': 2357}, '4 PM': {'PV': 4905, 'UV': 2144}, '5 PM': {'PV': 4615, 'UV': 2211}, '6 PM': {'PV': 4234, 'UV': 2004}, '7 PM': {'PV': 4213, 'UV': 1900}, '8 PM': {'PV': 4260, 'UV': 1886}, '9 PM': {'PV': 3748, 'UV': 1865}, '10 PM': {'PV': 3334, 'UV': 1585}, '11 PM': {'PV': 2350, 'UV': 1198}}, 'Friday': {'12 AM': {'PV': 1358, 'UV': 752}, '1 AM': {'PV': 880, 'UV': 513}, '2 AM': {'PV': 781, 'UV': 420}, '3 AM': {'PV': 687, 'UV': 394}, '4 AM': {'PV': 872, 'UV': 465}, '5 AM': {'PV': 1495, 'UV': 635}, '6 AM': {'PV': 3537, 'UV': 1238}, '7 AM': {'PV': 6258, 'UV': 2227}, '8 AM': {'PV': 8944, 'UV': 3285}, '9 AM': {'PV': 8764, 'UV': 3670}, '10 AM': {'PV': 6785, 'UV': 3003}, '11 AM': {'PV': 6743, 'UV': 2950}, '12 PM': {'PV': 5905, 'UV': 2566}, '1 PM': {'PV': 5320, 'UV': 2268}, '2 PM': {'PV': 4440, 'UV': 2075}, '3 PM': {'PV': 4621, 'UV': 2156}, '4 PM': {'PV': 4307, 'UV': 2028}, '5 PM': {'PV': 3878, 'UV': 1954}, '6 PM': {'PV': 3809, 'UV': 1822}, '7 PM': {'PV': 3730, 'UV': 1795}, '8 PM': {'PV': 3561, 'UV': 1808}, '9 PM': {'PV': 3463, 'UV': 1764}, '10 PM': {'PV': 3214, 'UV': 1637}, '11 PM': {'PV': 2569, 'UV': 1321}}, 'Saturday': {'12 AM': {'PV': 1530, 'UV': 862}, '1 AM': {'PV': 966, 'UV': 582}, '2 AM': {'PV': 828, 'UV': 432}, '3 AM': {'PV': 582, 'UV': 304}, '4 AM': {'PV': 595, 'UV': 318}, '5 AM': {'PV': 813, 'UV': 390}, '6 AM': {'PV': 2343, 'UV': 800}, '7 AM': {'PV': 4298, 'UV': 1474}, '8 AM': {'PV': 6363, 'UV': 2198}, '9 AM': {'PV': 6058, 'UV': 2350}, '10 AM': {'PV': 5487, 'UV': 2040}, '11 AM': {'PV': 5037, 'UV': 2122}, '12 PM': {'PV': 4045, 'UV': 1861}, '1 PM': {'PV': 3524, 'UV': 1588}, '2 PM': {'PV': 3317, 'UV': 1582}, '3 PM': {'PV': 3353, 'UV': 1543}, '4 PM': {'PV': 3044, 'UV': 1536}, '5 PM': {'PV': 3316, 'UV': 1605}, '6 PM': {'PV': 3207, 'UV': 1557}, '7 PM': {'PV': 3075, 'UV': 1501}, '8 PM': {'PV': 3277, 'UV': 1558}, '9 PM': {'PV': 3286, 'UV': 1534}, '10 PM': {'PV': 2852, 'UV': 1327}, '11 PM': {'PV': 2078, 'UV': 1064}}, 'Sunday': {'12 AM': {'PV': 1358, 'UV': 716}, '1 AM': {'PV': 791, 'UV': 472}, '2 AM': {'PV': 691, 'UV': 345}, '3 AM': {'PV': 427, 'UV': 248}, '4 AM': {'PV': 425, 'UV': 230}, '5 AM': {'PV': 627, 'UV': 307}, '6 AM': {'PV': 1129, 'UV': 509}, '7 AM': {'PV': 1975, 'UV': 823}, '8 AM': {'PV': 3486, 'UV': 1369}, '9 AM': {'PV': 3748, 'UV': 1595}, '10 AM': {'PV': 3027, 'UV': 1509}, '11 AM': {'PV': 3252, 'UV': 1646}, '12 PM': {'PV': 2903, 'UV': 1421}, '1 PM': {'PV': 2504, 'UV': 1371}, '2 PM': {'PV': 2420, 'UV': 1351}, '3 PM': {'PV': 2308, 'UV': 1278}, '4 PM': {'PV': 2373, 'UV': 1320}, '5 PM': {'PV': 2695, 'UV': 1458}, '6 PM': {'PV': 2890, 'UV': 1406}, '7 PM': {'PV': 3066, 'UV': 1493}, '8 PM': {'PV': 3224, 'UV': 1499}, '9 PM': {'PV': 2939, 'UV': 1444}, '10 PM': {'PV': 2598, 'UV': 1227}, '11 PM': {'PV': 1548, 'UV': 849}}}


def max_min(l):
    # return max and min as object
    # {'max': xxx, 'min': xxx}
    the_max = max(l)
    the_min = min(l)
    median_point = round(statistics.median(l), 2)
    return {'max': the_max, 'min': the_min, 'median_point': median_point}


def process_omni_files(file_name):
    # read in file_name using utility_io
    # process by steps
    # add to dict data['uv'], data['pv]
    pass


def chunk_string(s, start, end):
    # return string as list of substrings
    # based on start, end markers
    the_list = []
    marker = {'start': start, 'end': end}
    for line in s.splitlines():
        if marker['start'] in line:
            temp_list = []
            temp_list.append(line)
        else:
            temp_list.append(line)
            if marker['end'] in line:
                the_list.append(temp_list)
    return the_list


def list_to_dict(l_of_l):
    # takes a list of lists of strings,
    # munges them into dict form we need for later
    the_list = []
    '''
    INCOMING DATA ...
    temp = [
        {'day': 'XXXday', 'times': [{'time': '12 AM', 'PV': 123, 'UV': 234}, {'time': '1 AM', 'PV': 123, 'UV': 234}]},
        {'day': 'XXXday', 'times': [{'time': '12 AM', 'PV': 345, 'UV': 342}, {'time': '1 AM', 'PV': 115, 'UV': 852}]},
    ]
    '''
    for l in l_of_l:
        date = (l[0].split(',')[0][6:]) + ' 2019'
        datetime_object = datetime.strptime(date, '%b %d %Y')
        day = calendar.day_name[datetime_object.weekday()]
        # first item in chunk is 12 AM data
        tmp = {}
        tmp['day'] = day
        tmp['times'] = []
        for s in l:
            time, pv, uv = s.split(',')
            if ('M ') in time:
                time = time[0:(time.find('M ') + 1)]
            tmp['times'].append({'time': time, 'PV': int(pv), 'UV': int(uv)})
        the_list.append(tmp)
    return the_list


def compact_data(d, days, hours):
    # reformat dict, from day-based to hour-based
    # in order to easily build

    '''
    if we start with
    'days': {}

    'Monday': {'total': {'PV}, '12 AM': {'PV': 1047, 'UV': 536}, '1 AM': {'PV': 645, 'UV': 358},...
    to ->
    {
    '12 AM': {'PV': [], 'UV': []},
    'total': {'PV': [], 'UV': []},
    }
    '''
    new_d = {}
    new_d['totals'] = {}
    new_d['totals']['max_min'] = {}
    new_hours = ['total'] + hours
    for hour in new_hours:
        new_d[hour] = {}
        new_d[hour]['PV'] = []
        new_d[hour]['UV'] = []
        for day in days:
            new_d[hour]['PV'].append(d[day][hour]['PV'])
            new_d[hour]['UV'].append(d[day][hour]['UV'])
    for day in days:
        new_d['totals']['max_min'][day] = {}
        new_d['totals']['max_min']['week_by_day'] = {}
        new_d['totals']['max_min'][day]['PV'] = max_min(d[day]['totals']['PV'])
        new_d['totals']['max_min'][day]['UV'] = max_min(d[day]['totals']['UV'])
        new_d['totals']['max_min']['week_by_day']['PV'] = max_min(new_d['total']['PV'])
        new_d['totals']['max_min']['week_by_day']['UV'] = max_min(new_d['total']['UV'])

    # 'totals': {
    #            'PV': [1..7], 'UV': [1...7 ],
    #            'max_min': {
    #                         'week': {'pv': {max': 456, 'min': 122}, 'uv': {max': 456, 'min': 122}},
    #                         'Monday': {'pv': {max': 456, 'min': 122}, 'uv': {max': 456, 'min': 122}},
    #                         'Tuesday': {'pv': {max': 456, 'min': 122}, 'uv': {max': 456, 'min': 122}},
    #                        }
    #           },
    # 'hours': { '12 AM': {'PV': [1...7], 'UV': [1...7]},
    #             '1 AM': {'PV': [1...7], 'UV': [1...7]}, }
    #
    # }
    return new_d


# ---------------
# [ MAIN ]
# ---------------

#TODO move all omniture parsing into a function
# create function for parsing 

days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']
am, pm, hours = [], [], []
for hour in range(1, 13):
    am.append(str(hour) + ' AM')
    pm.append(str(hour) + ' PM')
hours = am[-1:] + am[:-1] + pm[-1:] + pm[:-1]

files = ['spectator_pv_uv.csv', 'record_pv_uv.csv', 'standard_pv_uv.csv', 'examiner_pv_uv.csv']
file_name = files[0]

data = utils_io.get_file(file_name, ['data_in', 'heatmap'])

# process omni CSV files (days/hours, page views, unique visitors)
# first, turn into a list of lines grouped by date
step_1 = chunk_string(data, '12 AM', '11 PM')
print("=======\n", step_1)
# create list of objects, each date having its set of times and values
# and add what day of week each group belongs to
step_2 = list_to_dict(step_1)
print("=======\nStep 2\n=======\n", step_2)

# STEP 3
# create dict, each day of week having pv and uv totals for each time
result = {}
for day in days:
    result[day] = {}
    day_list = [x for x in step_2 if x['day'] == day]
    for item in day_list:
        for time in item['times']:
            if time['time'] not in result[day]:
                result[day][time['time']] = {}
            if 'PV' in result[day][time['time']]:
                result[day][time['time']]['PV'] += time['PV']
            else:
                result[day][time['time']]['PV'] = time['PV']
            if 'UV' in result[day][time['time']]:
                result[day][time['time']]['UV'] += time['UV']
            else:
                result[day][time['time']]['UV'] = time['UV']
print("=======\nStep 3\n=======\n", result)

# STEP 4
# now create total for each day of week
# create list of hourly totals for each day of week
# and add to dict
for day in days:
    result[day]['total'] = {}
    result[day]['totals'] = {}
    PV = 0
    UV = 0
    PV_list = []
    UV_list = []
    # add up all the PV, UV for each time
    for hour in hours:
        PV_list.append(result[day][hour]['PV'])
        UV_list.append(result[day][hour]['UV'])
        PV += result[day][hour]['PV']
        UV += result[day][hour]['UV']
    result[day]['totals']['PV'] = PV_list
    result[day]['totals']['UV'] = UV_list
    result[day]['total']['PV'] = PV
    result[day]['total']['UV'] = UV
print("=======\nStep 4\n=======\n", result)

utils_io.put_file(json.dumps(result), 'heatmap_full_data.txt', ['data_out'])

# pivot, switching columns and rows so that we have a dict of:
# '12 AM': {'Monday': {'PV': 123, 'UV': 234'}, 'Tuesday': {'PV': 123, 'UV': 234'}, ...}
# 'total': {'Monday': {'PV': 1235, 'UV': 2345'}, 'Tuesday': {'PV': 1234, 'UV': 2345'}...}

# determine opacity for a value in a series
# WE ONLY NEED current value + series max + series min.

# STEP 5
new_result = compact_data(result, days, hours)
print("=======\nStep 5\n=======\n", new_result)

# STEP 6
final = {}
final['day_totals'] = new_result['total']
final['max_totals'] = new_result['totals']['max_min']
del new_result['total']
del new_result['totals']
final['hours'] = {}
for p, v in new_result.items():
    final['hours'][p] = v

final['max_totals']['week_whole'] = {}
final['max_totals']['week_whole']['PV'] = []
final['max_totals']['week_whole']['UV'] = []
for p, v in final['hours'].items():
    final['max_totals']['week_whole']['PV'] += v['PV']
    final['max_totals']['week_whole']['UV'] += v['UV']
final['max_totals']['week_whole']['PV'] = max_min(final['max_totals']['week_whole']['PV'])
final['max_totals']['week_whole']['UV'] = max_min(final['max_totals']['week_whole']['UV'])


print("=======\nStep 6\n=======\n", final)

utils_io.put_file(json.dumps(final), 'heatmap_compact_data.txt', ['data_out'])

html = template('heat_maps.html', data=final, hours=hours, days=days)
print("=======\n", html)

utils_io.put_file(html, 'heatmap.html', ['data_reports'])

'''
{'Monday': {'12 AM': {'PV': 1047, 'UV': 536}, '1 AM': {'PV': 645, 'UV': 358}, '2 AM': {'PV': 504, 'UV': 265}, '3 AM': {'PV': 506, 'UV': 268}, '4 AM': {'PV': 553, 'UV': 256}, '5 AM': {'PV': 1221, 'UV': 510}, '6 AM': {'PV': 3356, 'UV': 1169}, '7 AM': {'PV': 5110, 'UV': 1851}, '8 AM': {'PV': 6749, 'UV': 2444}, '9 AM': {'PV': 6758, 'UV': 2623}, '10 AM': {'PV': 5434, 'UV': 2340}, '11 AM': {'PV': 6213, 'UV': 2773}, '12 PM': {'PV': 6585, 'UV': 2771}, '1 PM': {'PV': 6244, 'UV': 2685}, '2 PM': {'PV': 5245, 'UV': 2475}, '3 PM': {'PV': 5624, 'UV': 2452}, '4 PM': {'PV': 4690, 'UV': 2226}, '5 PM': {'PV': 4581, 'UV': 2304}, '6 PM': {'PV': 4436, 'UV': 2183}, '7 PM': {'PV': 4032, 'UV': 2170}, '8 PM': {'PV': 4358, 'UV': 2256}, '9 PM': {'PV': 3931, 'UV': 2009}, '10 PM': {'PV': 2953, 'UV': 1657}, '11 PM': {'PV': 2100, 'UV': 1070}},
'''

# we need data in format
# {

# 'totals': {
#            'PV': [1..7], 'UV': [1...7 ],
#            'max_min': {
#                         'week': {'pv': {max': 456, 'min': 122}, 'uv': {max': 456, 'min': 122}},
#                         'Monday': {'pv': {max': 456, 'min': 122}, 'uv': {max': 456, 'min': 122}},
#                         'Tuesday': {'pv': {max': 456, 'min': 122}, 'uv': {max': 456, 'min': 122}},
#                        }
#           },
# 'hours': { '12 AM': {'PV': [1...7], 'UV': [1...7]},
#             '1 AM': {'PV': [1...7], 'UV': [1...7]}, }
#
# }
