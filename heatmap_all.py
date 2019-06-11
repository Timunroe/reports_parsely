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

test_data = '''12 AM Jan 1,666,349
1 AM,523,235
2 AM,330,164
3 AM,255,127
4 AM,236,146
5 AM,414,211
6 AM,870,332
7 AM,1635,712
8 AM,2643,1230
9 AM,3291,1567
10 AM,3223,1631
11 AM,2503,1356
12 PM Jan 1,2293,1253
1 PM,2015,1068
2 PM,1870,996
3 PM,1834,982
4 PM,1894,868
5 PM,1597,835
6 PM,1641,833
7 PM,1642,847
8 PM,1789,850
9 PM,1544,767
10 PM,1352,598
11 PM,799,397
12 AM Feb 13,5884,3527
1 AM,3734,2310
2 AM,2415,1596
3 AM,2439,1489
4 AM,3136,1755
5 AM,6529,3547
6 AM,17653,7520
7 AM,23038,10130
8 AM,22995,8976
9 AM,22849,9524
10 AM,20552,9550
11 AM,17757,8272
12 PM Feb 13,20609,10093
1 PM,17945,9162
2 PM,16060,8153
3 PM,15262,7557
4 PM,14351,6994
5 PM,16372,8410
6 PM,16695,8952
7 PM,15663,8490
8 PM,16175,8759
9 PM,16583,9326
10 PM,14039,7949
11 PM,9231,5164
'''

# ---------------
# [ FUNCTIONS ]
# ---------------


def split_text(s):
    temps = s.replace('12 AM', '*12 AM')
    temps = (temps.split('*'))[1:]
    temps = [x.splitlines() for x in temps]
    # print(temps)
    new_list = []
    for record in temps:
        temp = {}
        temp['day'] = get_day_name((record[0].split(','))[0])
        temp['pv'] = [int((x.split(','))[1]) for x in record]
        temp['uv'] = [int((x.split(','))[2]) for x in record]
        new_list.append(temp)
    print('*** Step 1 ***\n', new_list)
    return new_list


def max_min(l):
    the_max = max(l)
    the_min = min(l)
    median_point = round(statistics.median(l), 2)
    return {'max': the_max, 'min': the_min, 'median_point': median_point}


def get_day_name(s):
    date = s[6:] + ' 2019'
    datetime_object = datetime.strptime(date, '%b %d %Y')
    day_name = calendar.day_name[datetime_object.weekday()]
    return day_name


def process_omni_files(file_name):
    data = utils_io.get_file(file_name, ['data_in', 'heatmap'])
    return split_text(data)


# ---------------
# [ VARIABLES ]
# ---------------

final_data = {'Monday': {'12 AM': {'PV': 1047, 'UV': 536}, '1 AM': {'PV': 645, 'UV': 358}, '2 AM': {'PV': 504, 'UV': 265}, '3 AM': {'PV': 506, 'UV': 268}, '4 AM': {'PV': 553, 'UV': 256}, '5 AM': {'PV': 1221, 'UV': 510}, '6 AM': {'PV': 3356, 'UV': 1169}, '7 AM': {'PV': 5110, 'UV': 1851}, '8 AM': {'PV': 6749, 'UV': 2444}, '9 AM': {'PV': 6758, 'UV': 2623}, '10 AM': {'PV': 5434, 'UV': 2340}, '11 AM': {'PV': 6213, 'UV': 2773}, '12 PM': {'PV': 6585, 'UV': 2771}, '1 PM': {'PV': 6244, 'UV': 2685}, '2 PM': {'PV': 5245, 'UV': 2475}, '3 PM': {'PV': 5624, 'UV': 2452}, '4 PM': {'PV': 4690, 'UV': 2226}, '5 PM': {'PV': 4581, 'UV': 2304}, '6 PM': {'PV': 4436, 'UV': 2183}, '7 PM': {'PV': 4032, 'UV': 2170}, '8 PM': {'PV': 4358, 'UV': 2256}, '9 PM': {'PV': 3931, 'UV': 2009}, '10 PM': {'PV': 2953, 'UV': 1657}, '11 PM': {'PV': 2100, 'UV': 1070}}, 'Tuesday': {'12 AM': {'PV': 2171, 'UV': 1301}, '1 AM': {'PV': 1727, 'UV': 996}, '2 AM': {'PV': 1281, 'UV': 739}, '3 AM': {'PV': 947, 'UV': 556}, '4 AM': {'PV': 1069, 'UV': 590}, '5 AM': {'PV': 1836, 'UV': 855}, '6 AM': {'PV': 4366, 'UV': 1727}, '7 AM': {'PV': 8148, 'UV': 2806}, '8 AM': {'PV': 11078, 'UV': 4111}, '9 AM': {'PV': 11200, 'UV': 4477}, '10 AM': {'PV': 9720, 'UV': 4283}, '11 AM': {'PV': 9870, 'UV': 4611}, '12 PM': {'PV': 9989, 'UV': 4562}, '1 PM': {'PV': 7940, 'UV': 3824}, '2 PM': {'PV': 7438, 'UV': 3610}, '3 PM': {'PV': 7696, 'UV': 3729}, '4 PM': {'PV': 7420, 'UV': 3743}, '5 PM': {'PV': 7615, 'UV': 3958}, '6 PM': {'PV': 7878, 'UV': 4084}, '7 PM': {'PV': 7436, 'UV': 3825}, '8 PM': {'PV': 7771, 'UV': 3766}, '9 PM': {'PV': 6773, 'UV': 3511}, '10 PM': {'PV': 5714, 'UV': 2907}, '11 PM': {'PV': 4004, 'UV': 2063}}, 'Wednesday': {'12 AM': {'PV': 1104, 'UV': 574}, '1 AM': {'PV': 740, 'UV': 412}, '2 AM': {'PV': 629, 'UV': 322}, '3 AM': {'PV': 509, 'UV': 285}, '4 AM': {'PV': 533, 'UV': 280}, '5 AM': {'PV': 1193, 'UV': 477}, '6 AM': {'PV': 3027, 'UV': 954}, '7 AM': {'PV': 5520, 'UV': 1644}, '8 AM': {'PV': 7069, 'UV': 2409}, '9 AM': {'PV': 7621, 'UV': 2671}, '10 AM': {'PV': 6828, 'UV': 2544}, '11 AM': {'PV': 6300, 'UV': 2626}, '12 PM': {'PV': 6513, 'UV': 2620}, '1 PM': {'PV': 5282, 'UV': 2236}, '2 PM': {'PV': 4871, 'UV': 2130}, '3 PM': {'PV': 4824, 'UV': 2068}, '4 PM': {'PV': 4342, 'UV': 2051}, '5 PM': {'PV': 4381, 'UV': 1985}, '6 PM': {'PV': 3898, 'UV': 1846}, '7 PM': {'PV': 3814, 'UV': 1792}, '8 PM': {'PV': 4097, 'UV': 1887}, '9 PM': {'PV': 3614, 'UV': 1694}, '10 PM': {'PV': 3184, 'UV': 1413}, '11 PM': {'PV': 1921, 'UV': 959}}, 'Thursday': {'12 AM': {'PV': 1418, 'UV': 661}, '1 AM': {'PV': 865, 'UV': 486}, '2 AM': {'PV': 706, 'UV': 355}, '3 AM': {'PV': 445, 'UV': 285}, '4 AM': {'PV': 625, 'UV': 326}, '5 AM': {'PV': 1319, 'UV': 535}, '6 AM': {'PV': 2770, 'UV': 1061}, '7 AM': {'PV': 4981, 'UV': 1862}, '8 AM': {'PV': 6974, 'UV': 2470}, '9 AM': {'PV': 7484, 'UV': 2865}, '10 AM': {'PV': 6460, 'UV': 2622}, '11 AM': {
    'PV': 6561, 'UV': 2971}, '12 PM': {'PV': 6497, 'UV': 2738}, '1 PM': {'PV': 4883, 'UV': 2346}, '2 PM': {'PV': 4926, 'UV': 2191}, '3 PM': {'PV': 5411, 'UV': 2357}, '4 PM': {'PV': 4905, 'UV': 2144}, '5 PM': {'PV': 4615, 'UV': 2211}, '6 PM': {'PV': 4234, 'UV': 2004}, '7 PM': {'PV': 4213, 'UV': 1900}, '8 PM': {'PV': 4260, 'UV': 1886}, '9 PM': {'PV': 3748, 'UV': 1865}, '10 PM': {'PV': 3334, 'UV': 1585}, '11 PM': {'PV': 2350, 'UV': 1198}}, 'Friday': {'12 AM': {'PV': 1358, 'UV': 752}, '1 AM': {'PV': 880, 'UV': 513}, '2 AM': {'PV': 781, 'UV': 420}, '3 AM': {'PV': 687, 'UV': 394}, '4 AM': {'PV': 872, 'UV': 465}, '5 AM': {'PV': 1495, 'UV': 635}, '6 AM': {'PV': 3537, 'UV': 1238}, '7 AM': {'PV': 6258, 'UV': 2227}, '8 AM': {'PV': 8944, 'UV': 3285}, '9 AM': {'PV': 8764, 'UV': 3670}, '10 AM': {'PV': 6785, 'UV': 3003}, '11 AM': {'PV': 6743, 'UV': 2950}, '12 PM': {'PV': 5905, 'UV': 2566}, '1 PM': {'PV': 5320, 'UV': 2268}, '2 PM': {'PV': 4440, 'UV': 2075}, '3 PM': {'PV': 4621, 'UV': 2156}, '4 PM': {'PV': 4307, 'UV': 2028}, '5 PM': {'PV': 3878, 'UV': 1954}, '6 PM': {'PV': 3809, 'UV': 1822}, '7 PM': {'PV': 3730, 'UV': 1795}, '8 PM': {'PV': 3561, 'UV': 1808}, '9 PM': {'PV': 3463, 'UV': 1764}, '10 PM': {'PV': 3214, 'UV': 1637}, '11 PM': {'PV': 2569, 'UV': 1321}}, 'Saturday': {'12 AM': {'PV': 1530, 'UV': 862}, '1 AM': {'PV': 966, 'UV': 582}, '2 AM': {'PV': 828, 'UV': 432}, '3 AM': {'PV': 582, 'UV': 304}, '4 AM': {'PV': 595, 'UV': 318}, '5 AM': {'PV': 813, 'UV': 390}, '6 AM': {'PV': 2343, 'UV': 800}, '7 AM': {'PV': 4298, 'UV': 1474}, '8 AM': {'PV': 6363, 'UV': 2198}, '9 AM': {'PV': 6058, 'UV': 2350}, '10 AM': {'PV': 5487, 'UV': 2040}, '11 AM': {'PV': 5037, 'UV': 2122}, '12 PM': {'PV': 4045, 'UV': 1861}, '1 PM': {'PV': 3524, 'UV': 1588}, '2 PM': {'PV': 3317, 'UV': 1582}, '3 PM': {'PV': 3353, 'UV': 1543}, '4 PM': {'PV': 3044, 'UV': 1536}, '5 PM': {'PV': 3316, 'UV': 1605}, '6 PM': {'PV': 3207, 'UV': 1557}, '7 PM': {'PV': 3075, 'UV': 1501}, '8 PM': {'PV': 3277, 'UV': 1558}, '9 PM': {'PV': 3286, 'UV': 1534}, '10 PM': {'PV': 2852, 'UV': 1327}, '11 PM': {'PV': 2078, 'UV': 1064}}, 'Sunday': {'12 AM': {'PV': 1358, 'UV': 716}, '1 AM': {'PV': 791, 'UV': 472}, '2 AM': {'PV': 691, 'UV': 345}, '3 AM': {'PV': 427, 'UV': 248}, '4 AM': {'PV': 425, 'UV': 230}, '5 AM': {'PV': 627, 'UV': 307}, '6 AM': {'PV': 1129, 'UV': 509}, '7 AM': {'PV': 1975, 'UV': 823}, '8 AM': {'PV': 3486, 'UV': 1369}, '9 AM': {'PV': 3748, 'UV': 1595}, '10 AM': {'PV': 3027, 'UV': 1509}, '11 AM': {'PV': 3252, 'UV': 1646}, '12 PM': {'PV': 2903, 'UV': 1421}, '1 PM': {'PV': 2504, 'UV': 1371}, '2 PM': {'PV': 2420, 'UV': 1351}, '3 PM': {'PV': 2308, 'UV': 1278}, '4 PM': {'PV': 2373, 'UV': 1320}, '5 PM': {'PV': 2695, 'UV': 1458}, '6 PM': {'PV': 2890, 'UV': 1406}, '7 PM': {'PV': 3066, 'UV': 1493}, '8 PM': {'PV': 3224, 'UV': 1499}, '9 PM': {'PV': 2939, 'UV': 1444}, '10 PM': {'PV': 2598, 'UV': 1227}, '11 PM': {'PV': 1548, 'UV': 849}}}

days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']
am, pm, hours = [], [], []
for hour in range(1, 13):
    am.append(str(hour) + ' AM')
    pm.append(str(hour) + ' PM')
hours = am[-1:] + am[:-1] + pm[-1:] + pm[:-1]
records, result = {}, {}

files = ['spectator_pv_uv.csv', 'record_pv_uv.csv',
         'standard_pv_uv.csv', 'examiner_pv_uv.csv']

# ---------------
# [ MAIN ]
# ---------------

file_name = files[0]
# STEP 1 ========
result['data'] = process_omni_files(file_name)
# result['data'] = split_text(test_data)
# print('*** Step 1 ***\n', result)

# WEEK MAX-MIN STATS (including each day's hourly totals)
pv_list = [x['pv'] for x in result['data']]
uv_list = [x['uv'] for x in result['data']]

result['week_pv_stats'] = max_min([item for sublist in pv_list for item in sublist])
result['week_uv_stats'] = max_min([item for sublist in uv_list for item in sublist])

# TOTALS BY DAY
result['totals by day'] = {'pv': [], 'uv': []}
for day in days:
    result['totals by day']['pv'].append(sum([sum(record['pv']) for record in result['data'] if record['day'] == day]))
    result['totals by day']['pv_stats'] = max_min(result['totals by day']['pv'])
    result['totals by day']['uv'].append(sum([sum(record['uv']) for record in result['data'] if record['day'] == day]))
    result['totals by day']['uv_stats'] = max_min(result['totals by day']['uv'])

# HOURS BY DAY LIST
result['hours_by_day'] = []
for idx, hour in enumerate(hours):
    obj = {'hour': hour, 'pv': [], 'uv': []}
    for day in days:
        obj['pv'].append(sum([record['pv'][idx] for record in result['data'] if record['day'] == day]))
        obj['uv'].append(sum([record['uv'][idx] for record in result['data'] if record['day'] == day]))
    result['hours_by_day'].append(obj)

# DAY BY HOURS LIST
result['days_by_hours'] = []
for day in days:
    obj = {'day': day, 'pv': [], 'uv': []}
    for idx, hour in enumerate(hours):
        obj['pv'].append(sum([record['pv'][idx] for record in result['data'] if record['day'] == day]))
        obj['pv_stats'] = max_min(obj['pv'])
        obj['uv'].append(sum([record['uv'][idx] for record in result['data'] if record['day'] == day]))
        obj['uv_stats'] = max_min(obj['uv'])
    result['days_by_hours'].append(obj)

print('*** Result ***\n', result)


utils_io.put_file(json.dumps(result), 'heatmap_full_data.txt', ['data_out'])

# html = template('heat_maps.html', data=data, hours=hours, days=days)
# utils_io.put_file(html, 'heatmap.html', ['data_reports'])

# data['traffic'] = process_omni_files(file_name)

'''
{'Monday': {'12 AM': {'PV': 1047, 'UV': 536}, '1 AM': {'PV': 645, 'UV': 358}, '2 AM': {'PV': 504, 'UV': 265}, '3 AM': {'PV': 506, 'UV': 268}, '4 AM': {'PV': 553, 'UV': 256}, '5 AM': {'PV': 1221, 'UV': 510}, '6 AM': {'PV': 3356, 'UV': 1169}, '7 AM': {'PV': 5110, 'UV': 1851}, '8 AM': {'PV': 6749, 'UV': 2444}, '9 AM': {'PV': 6758, 'UV': 2623}, '10 AM': {'PV': 5434, 'UV': 2340}, '11 AM': {'PV': 6213, 'UV': 2773}, '12 PM': {'PV': 6585, 'UV': 2771}, '1 PM': {'PV': 6244, 'UV': 2685}, '2 PM': {'PV': 5245, 'UV': 2475}, '3 PM': {'PV': 5624, 'UV': 2452}, '4 PM': {'PV': 4690, 'UV': 2226}, '5 PM': {'PV': 4581, 'UV': 2304}, '6 PM': {'PV': 4436, 'UV': 2183}, '7 PM': {'PV': 4032, 'UV': 2170}, '8 PM': {'PV': 4358, 'UV': 2256}, '9 PM': {'PV': 3931, 'UV': 2009}, '10 PM': {'PV': 2953, 'UV': 1657}, '11 PM': {'PV': 2100, 'UV': 1070}},
'''
