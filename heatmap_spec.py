import pandas as pd


# file_name = "reports/heatmap.csv"
file_name = 'reports/standard-local-top-posts-byPV-Dec-Feb.csv'
# print(list(df.columns.values))
cols_to_keep = [
    'URL',
    'Title',
    'Publish date',
    'Authors',
    'Section',
    'Visitors',
    'Views',
    'Engaged minutes',
]

df = pd.read_csv(file_name,
                 usecols=cols_to_keep,
                 keep_default_na=False,
                 na_values='0')

df.columns = df.columns.str.replace('\xa0', ' ')

# SOME COLUMNS HAVE NUMBERS IN STRING TYPE
# cols_to_fix = ["Search refs", "Internal refs", "Other refs", "Social refs", "Fb refs", "Tw refs", "Li refs", "Pi refs", "Social interactions", "Fb interactions", "Tw interactions"]
# df[cols_to_fix] = df[cols_to_fix].apply(pd.to_numeric)

# extract time stamp, add columns for DAY and TIME
# df['Day'] = (df['change'] > 0).astype(int)
df['Publish date'] = pd.to_datetime(df['Publish date'])
df['Publish fix'] = df['Publish date'] + pd.Timedelta('5 hours')
df['weekday'] = df['Publish fix'].dt.dayofweek
df['time'] = df['Publish fix'].dt.hour
# print(df['Publish date'])
# print(df['Publish fix'])
# print(df['weekday'])
# print(df['time'])
new = df[['weekday', 'time']].copy()
# need to get sums of items with same weekday AND time
# so weekday 1 at time 4 will be total X

new_records = new.to_dict(orient='records')
heat_data = {
    '0': {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
    },
    '1': {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
    },
    '2': {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
    },
    '3': {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
    },
    '4': {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
    },
    '5': {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
    },
    '6': {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
    },
}

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
print(s)
# print(heat_data)
# print(df.dtypes)

# how to sum using dataframe?
# make new dataframe columns ...
# filter on weekday column for each weekday number, and specific hour
