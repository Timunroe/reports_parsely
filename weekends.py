import pathlib
import sys
import re
import csv
import pandas as pd
from io import StringIO
# mine
import utils_num_new as u

# FILE NAMES
filenames = ['star', 'spectator', 'record', 'standard', 'review', 'tribune', 'examiner', 'durham']

# SITE STATS
site_cols_keep = [
    'Date',
    'Visitors',
    'Views',
    'Engaged minutes',
    'New Posts',
    'Social interactions',
    'Fb interactions',
    'Tw interactions',
    # 'Li interactions',
    'Desktop views',
    'Mobile views',
    'Tablet views',
    'Search refs',
    'Internal refs',
    'Other refs',
    'Direct refs',
    'Social refs',
    'Fb refs',
    'Tw refs',
    # 'Li refs',
    'New vis.',
    'Views new vis.',
    'Avg. views new vis.',
    'Minutes New Vis.',
    'Avg. minutes new vis.',
    'Returning vis.',
    'Views ret. vis.',
    'Avg. views ret. vis.',
    'Minutes Ret. Vis.',
    'Avg. minutes ret. vis.',
]


def process_csv(file_name, cols_to_keep=None, parsely_fix=True):
    if parsely_fix:
        path = pathlib.Path.cwd() / 'data_in' / file_name
        fixed_csv = path.read_text().replace('.0', '').replace('\xa0', ' ')\
            .replace(',,,,', ',0,0,0,').replace(',,,', ',0,0,')\
            .replace(',,', ',0,').replace(',\n', ',0\n')
        # TEST POINT
        # print(fixed_csv)
    if cols_to_keep:
        df = pd.read_csv(StringIO(fixed_csv), usecols=cols_to_keep)
        # df = pd.read_csv(pd.compat.StringIO(fixed_csv), usecols=cols_to_keep)
        # df = pd.read_csv(file_name, usecols=cols_to_keep, keep_default_na=False, na_values='0')
    else:
        df = pd.read_csv(file_name,
                         keep_default_na=False,
                         na_values='0')
    # fixes for Parsely
    # df.columns = df.columns.str.replace('\xa0', ' ')
    # do i need this after the fixes at start of function?
    # cols_to_fix = ["Search refs", "Internal refs", "Other refs", "Social refs", "Fb refs", "Tw refs", "Li refs", "Pi refs", "Social interactions", "Fb interactions", "Tw interactions"]
    # df[cols_to_fix] = df[cols_to_fix].apply(pd.to_numeric)
    return df


# MAIN START
s = f'''PV data for June 17-Sept. 17\n'''
for file in filenames:
    df = process_csv(f'{file}_weekend.csv', site_cols_keep, True)
    #  convert 'date' column to real date object
    df['Date'] = pd.to_datetime(df['Date'])
    # add a 'dow' day of week column
    df['DOW'] = df['Date'].dt.day_name()
    # reverse sort on Date because that's how Pandas likes to roll
    df_site = df.sort_values(by=['Date'])
    # print(df_site['DOW'])
    df_weekend = df_site[(df_site['DOW'] == 'Saturday') | (df_site['DOW'] == 'Sunday')]
    df_week = df_site[(df_site['DOW'] != 'Saturday') & (df_site['DOW'] != 'Sunday')]
    # sat = df_weekend[(df_weekend['DOW'] == 'Saturday')]
    # sun = df_weekend[(df_weekend['DOW'] == 'Sunday')]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_totals = []
    for day in days:
        day_totals.append((df_site[(df_site['DOW'] == day)])['Views'].sum())
    # print(day_totals)
    # weeks_no = sat['DOW'].count()
    weeks_no = (df_site[(df_site['DOW'] == 'Saturday')])['DOW'].count()
    # print("Weeks count is: ", weeks_no)
    pv_total = df_site['Views'].sum()

    # print('Saturday views:\n', sat['Views'])
    # print(sat['New Posts'].mean())
    posts_total = df_site['New Posts'].sum()
    day_posts = []
    for day in days:
        day_posts.append((df_site[(df_site['DOW'] == day)])['New Posts'].sum())

    week_avg = (df_site['Views'].sum() / weeks_no)
    weekdays_avg = (df_week['Views'].sum()) / weeks_no
    weekend_avg = (df_weekend['Views'].sum()) / weeks_no
    posts_avg = df_weekend['New Posts'].mean()
    weekday_avg = df_week['Views'].mean()
    s += f'''{file.upper()}:\nShould track total new articles and news-local articles'''
    s += f'''Weekly breakdown: '''
    s += f'''weekdays {u.percentage(weekdays_avg, week_avg, 1)}% ({u.humanize(weekdays_avg, 0)}) | '''
    s += f'''weekend {u.percentage(weekend_avg, week_avg, 1)}% ({u.humanize(weekend_avg, 0)})\n'''
    # s += f'''Weekend New Posts avg: {int(round(posts_avg,0))}\n'''
    s += f'''--------------------------------------------------------\n'''
    s += f'''Daily  |   M  |   T  |   W  |  Th  |   F  |  Sa  |  Su\n'''
    s += f'''PV %   '''
    for item in day_totals:
        s += f'''|{str(u.percentage(item, pv_total, 1)).rjust(5)} '''
    s += f'''\nPost % '''
    for item in day_posts:
        s += f'''|{str(u.percentage(item, posts_total, 1)).rjust(5)} '''
    s += f'''\n--------------------------------------------------------\n\n'''
    # print(df_site[['DOW','Views']].values.tolist())

print(s)
