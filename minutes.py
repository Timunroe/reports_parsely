import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import pathlib
sns.set()

rcParams.update({'figure.autolayout': True})


def process_csv(file_name, freq):
    path = pathlib.Path.cwd() / 'data_in' / f'{freq}' / file_name
    fixed_csv = path.read_text().replace('.0', '').replace(
        '\xa0', ' ').replace(',,,,', ',0,0,0,').replace(',,,', ',0,0,').replace(
        ',,', ',0,').replace(',\n', ',0\n')
    # TEST POINT
    # print(fixed_csv)
    return pd.read_csv(pd.compat.StringIO(fixed_csv))


file_name = "section_local_minutes.csv"
freq = 'weekly'

df = process_csv(file_name, freq)
df['Date'] = pd.to_datetime(df['Date'])

for x in ['examiner', 'spec', 'standard', 'tribune', 'record', 'review']:
    df_test = df.copy()
    df_test = df_test[df_test['Site'].str.contains(x)].sort_values(by=['Date'])
    df_test['Post avg'] = round((df_test['Minutes'] / df_test['New Posts']), 1)
    df_test['Minutes rm'] = df_test['Minutes'].rolling(
        window=13, center=False).mean()
    print(df_test['Minutes rm'])
    df_test['New Posts rm'] = df_test['New Posts'].rolling(
        window=13, center=False).mean()
    df_test['Post avg rm'] = df_test['Post avg'].rolling(
        window=13, center=False).mean()

    # close
    plt.close('all')

    plt.figure()
    df_test[df_test['Minutes rm'].notnull()].plot(
        x='Date', y='Minutes rm', kind='line')
    # plt.tight_layout()
    plt.grid(b=True, which='major', axis='y')
    plt.xlabel('Week')
    plt.ylabel('Post avg')
    plt.savefig(f'data_out/s_minutes_{x}.png')

    # close
    plt.close('all')

    plt.figure()
    df_test[df_test['New Posts rm'].notnull()].plot(
        x='Date', y=['New Posts rm'], kind='line')
    # plt.tight_layout()
    plt.grid(b=True, which='major', axis='y')
    plt.xlabel('Week')
    plt.ylabel('Posts')
    plt.savefig(f'data_out/s_posts_{x}.png')
