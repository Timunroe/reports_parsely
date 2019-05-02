import pandas as pd
import pathlib
import sys
from utils import utils_io
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib import rcParams

sns.set()
rcParams.update({'figure.autolayout': True})
plt.rcParams['axes.labelweight'] = 'bold'

filename1 = 'spectator_heat_publish.csv'
filename2 = 'record_heat_publish.csv'
filename3 = 'examiner_heat_publish.csv'
filename4 = 'niagara_heat_publish.csv'

# VISITOR/PAGE VIEWS TIMES






# PUBLISHING TIMES

# print(list(df.columns.values))
cols_to_keep = [
    'Publish date',
    'Authors',
    'Section',
    'Tags',
    'Visitors',
    'Views',
    'Engaged minutes',
]


def get_day_of_week(x):
    days_arr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return days_arr[x]


def get_regular_time(x):
    hours_arr = ['12a', '1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a',
                 '10a', '11a', '12p', '1p', '2p', '3p', '4p', '5p', '6p',
                 '7p', '8p', '9p', '10p', '11p']
    return hours_arr[x]


def process_csv(filename, folders=None, cols_to_keep=None):
    if folders:
        if not isinstance(folders, list):
            print("Folders paramaeter MUST be a list!")
            sys.exit()
        p = pathlib.Path.cwd().joinpath(*folders)
    else:
        p = pathlib.Path.cwd()
    path = p.joinpath(filename)
    csv_data = path.read_text().replace('.0', '')\
        .replace('\xa0', ' ')\
        .replace(',,,,', ',0,0,0,').replace(',,,', ',0,0,')\
        .replace(',,', ',0,').replace(',\n', ',0\n')
    # TEST POINT
    # print(fixed_csv)
    if cols_to_keep:
        df = pd.read_csv(pd.compat.StringIO(csv_data), usecols=cols_to_keep)
    else:
        df = pd.read_csv(pd.compat.StringIO(csv_data))
    return df


def fix_time(d):
    if (pd.to_datetime('2018-11-03') < d < pd.to_datetime('2019-03-10')):
        return d + pd.Timedelta('5 hours')
    else:
        return d + pd.Timedelta('4 hours')


def plot_it(filename):
    # close
    plt.close('all')
    df_new = process_csv(filename, ['data_out'])
    print(df_new.dtypes)
    df_new.set_index('hour', inplace=True)
    plt.figure(figsize=(10, 10))
    sns.heatmap(df_new, annot=True, fmt="d", linewidths=.5, yticklabels=2)
    plt.yticks(rotation=0)
    plt.savefig('data_out/heat.png')


# [MAIN]--------------------------------
df = process_csv(filename1, ['data_in', 'heatmap'], cols_to_keep)

# SOME COLUMNS HAVE NUMBERS IN STRING TYPE
# df[cols_to_fix] = df[cols_to_fix].apply(pd.to_numeric)

# extract time stamp, add columns for DAY and TIME
# df['Day'] = (df['change'] > 0).astype(int)
df['Publish date'] = pd.to_datetime(df['Publish date'])
# BEWARE TIME CHANGE
# before March 10, add 5 hours
# after March 10, add 4 hours
# df['Publish fix'] = df['Publish date'] + pd.Timedelta('4 hours')
df['Publish fix'] = df['Publish date'].apply(fix_time)
df['weekday'] = df['Publish fix'].dt.dayofweek
df['time'] = df['Publish fix'].dt.hour
# print(df.dtypes)
# useful_columns = ['weekday', 'time']
# df.loc[:, useful_columns].to_csv('data_out/new.csv')
# for every hour of very day, we need a sum

# we're looping hours first, then days
'''
hour, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
0     33
1     3
'''
s = f'''hour,Mon,Tue,Wed,Thu,Fri,Sat,Sun'''
for x in range(24):
    # loop over days
    s += f'''\n{get_regular_time(x)}'''
    for y in range(7):
        # Add filters here
        # all content, page views greater than 19
        posts = df[(df['weekday'] == y) & (df['time'] == x) & (df['Views'] > 19)]
        # primary pub
        # posts = df[(df['weekday'] == y) & (df['time'] == x) & (df['Tags'].str.contains("primary_publication:hamiltonspectator"))]
        # primary pub AND news local
        # posts = df[(df['weekday'] == y) & (df['time'] == x) & (df['Tags'].str.contains("primary_publication:hamiltonspectator", regex=False)) & (df['Tags'].str.contains("news|local", regex=False))]
        s += f''',{posts.shape[0]}'''

utils_io.put_file(s, filename1, ['data_out'])

plot_it(filename1)

""" def blah():
    new_records = new.to_dict(orient='records')
    # [{'weekday': 1, 'time': 6}, {'weekday': 0, 'time': 7}, {'weekday': 1, 'time': 6}, {'weekday': 0, 'time': 8}, {'weekday': 4, 'time': 20}]
    for item in new_records:
        heat_data[str(item['weekday'])][str(item['time'])] += 1

    s = "0,1,2,3,4,5,6\n"
    for x in range(24):
        s += f'''{heat_data[str(0)][str(x)]},{heat_data[str(1)][str(x)]},{heat_data[str(2)][str(x)]},\
            {heat_data[str(3)][str(x)]},{heat_data[str(4)][str(x)]},{heat_data[str(5)][str(x)]},\
            {heat_data[str(6)][str(x)]}\n'''

    # print(heat_data['weekday']['1']['5'])
    articles_total = new['weekday'].count()

    print(f'Based on {articles_total} articles published during Dec. 2018 and Feb. 2019')
    print(s) """
