# from datetime import date
from datetime import datetime
import calendar

# time, PV, UV
data = '''12 AM Jan 1,1092,678
1 AM,1016,601
2 AM,757,428
3 AM,456,288
4 AM,454,273
5 AM,546,284
6 AM,888,453
7 AM,2208,873
8 AM,3458,1523
9 AM,4524,1909
10 AM,4241,1989
11 AM,4569,2181
12 PM Jan 1,3797,1900
1 PM,3225,1597
2 PM,2993,1529
3 PM,3026,1541
4 PM,3143,1564
5 PM,3555,1740
6 PM,3457,1636
7 PM,3168,1578
8 PM,3495,1581
9 PM,3151,1508
10 PM,2570,1241
11 PM,1836,911
12 AM Jan 2,1104,574
1 AM,740,412
2 AM,629,322
3 AM,509,285
4 AM,533,280
5 AM,1193,477
6 AM,3027,954
7 AM,5520,1644
8 AM,7069,2409
9 AM,7621,2671
10 AM,6828,2544
11 AM,6300,2626
12 PM Jan 2,6513,2620
1 PM,5282,2236
2 PM,4871,2130
3 PM,4824,2068
4 PM,4342,2051
5 PM,4381,1985
6 PM,3898,1846
7 PM,3814,1792
8 PM,4097,1887
9 PM,3614,1694
10 PM,3184,1413
11 PM,1921,959
12 AM Jan 3,1418,661
1 AM,865,486
2 AM,706,355
3 AM,445,285
4 AM,625,326
5 AM,1319,535
6 AM,2770,1061
7 AM,4981,1862
8 AM,6974,2470
9 AM,7484,2865
10 AM,6460,2622
11 AM,6561,2971
12 PM Jan 3,6497,2738
1 PM,4883,2346
2 PM,4926,2191
3 PM,5411,2357
4 PM,4905,2144
5 PM,4615,2211
6 PM,4234,2004
7 PM,4213,1900
8 PM,4260,1886
9 PM,3748,1865
10 PM,3334,1585
11 PM,2350,1198
12 AM Jan 4,1358,752
1 AM,880,513
2 AM,781,420
3 AM,687,394
4 AM,872,465
5 AM,1495,635
6 AM,3537,1238
7 AM,6258,2227
8 AM,8944,3285
9 AM,8764,3670
10 AM,6785,3003
11 AM,6743,2950
12 PM Jan 4,5905,2566
1 PM,5320,2268
2 PM,4440,2075
3 PM,4621,2156
4 PM,4307,2028
5 PM,3878,1954
6 PM,3809,1822
7 PM,3730,1795
8 PM,3561,1808
9 PM,3463,1764
10 PM,3214,1637
11 PM,2569,1321
12 AM Jan 5,1530,862
1 AM,966,582
2 AM,828,432
3 AM,582,304
4 AM,595,318
5 AM,813,390
6 AM,2343,800
7 AM,4298,1474
8 AM,6363,2198
9 AM,6058,2350
10 AM,5487,2040
11 AM,5037,2122
12 PM Jan 5,4045,1861
1 PM,3524,1588
2 PM,3317,1582
3 PM,3353,1543
4 PM,3044,1536
5 PM,3316,1605
6 PM,3207,1557
7 PM,3075,1501
8 PM,3277,1558
9 PM,3286,1534
10 PM,2852,1327
11 PM,2078,1064
12 AM Jan 6,1358,716
1 AM,791,472
2 AM,691,345
3 AM,427,248
4 AM,425,230
5 AM,627,307
6 AM,1129,509
7 AM,1975,823
8 AM,3486,1369
9 AM,3748,1595
10 AM,3027,1509
11 AM,3252,1646
12 PM Jan 6,2903,1421
1 PM,2504,1371
2 PM,2420,1351
3 PM,2308,1278
4 PM,2373,1320
5 PM,2695,1458
6 PM,2890,1406
7 PM,3066,1493
8 PM,3224,1499
9 PM,2939,1444
10 PM,2598,1227
11 PM,1548,849
12 AM Jan 7,1047,536
1 AM,645,358
2 AM,504,265
3 AM,506,268
4 AM,553,256
5 AM,1221,510
6 AM,3356,1169
7 AM,5110,1851
8 AM,6749,2444
9 AM,6758,2623
10 AM,5434,2340
11 AM,6213,2773
12 PM Jan 7,6585,2771
1 PM,6244,2685
2 PM,5245,2475
3 PM,5624,2452
4 PM,4690,2226
5 PM,4581,2304
6 PM,4436,2183
7 PM,4032,2170
8 PM,4358,2256
9 PM,3931,2009
10 PM,2953,1657
11 PM,2100,1070
12 AM Jan 8,1079,623
1 AM,711,395
2 AM,524,311
3 AM,491,268
4 AM,615,317
5 AM,1290,571
6 AM,3478,1274
7 AM,5940,1933
8 AM,7620,2588
9 AM,6676,2568
10 AM,5479,2294
11 AM,5301,2430
12 PM Jan 8,6192,2662
1 PM,4715,2227
2 PM,4445,2081
3 PM,4670,2188
4 PM,4277,2179
5 PM,4060,2218
6 PM,4421,2448
7 PM,4268,2247
8 PM,4276,2185
9 PM,3622,2003
10 PM,3144,1666
11 PM,2168,1152'''

# end result
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
    temp = [
        {'day': 'XXXday', 'times': [{'time': '12 AM', 'PV': 123, 'UV': 234}, {'time': '1 AM', 'PV': 123, 'UV': 234}]},
        {'date': 'xxx', 'times': [{'time': '12 AM', 'PV': 123, 'UV': 234}]},
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


# [ MAIN ]---------------

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hours = []
for hour in range(1, 13):
    hours.append(str(hour) + ' AM')
    hours.append(str(hour) + ' PM')

# process omni CSV files (days, hours, page views, unique visitors)
step_1 = chunk_string(data, '12 AM', '11 PM')
print("=======\n", step_1)
step_2 = list_to_dict(step_1)
print("=======\n", step_2)

result = {}
for day in days:
    result[day] = {}
    day_list = [x for x in step_2 if x['day'] == day]
    for z in day_list:
        for time in z['times']:
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
print("=======\n", result)

# import parsely CSV file that has publish times and dates
# where
