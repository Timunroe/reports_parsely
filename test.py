import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import pathlib
sns.set()

rcParams.update({'figure.autolayout': True})

# close
plt.close('all')

file_name = "Spectator_home_page_weekly.csv"
tw_file_name = 'spec_monthly_sm_posts.csv'
freq = 'weekly'

def process_csv(file_name, freq):
        path = pathlib.Path.cwd() / 'data_in' / f'{freq}' / file_name
        fixed_csv = path.read_text().replace('.0', '').replace('\xa0', ' ').replace(',,,,', ',0,0,0,').replace(',,,', ',0,0,').replace(',,', ',0,').replace(',\n', ',0\n')
        # TEST POINT
        # print(fixed_csv)
        return pd.read_csv(pd.compat.StringIO(fixed_csv))


df = process_csv(file_name, freq)

df['Week Starting'] = pd.to_datetime(df['Week Starting'])
# df['Avg'] = df['Articles'].expanding().mean()
# df.set_index('Week', inplace=True)
# print(df.dtypes)
# print(df.columns.values)
# print(df.head(3))

plt.figure()
df.plot(x='Week Starting', y=['Direct PV', 'HP PV', 'Visitors'], kind='line')
# plt.tight_layout()
plt.grid(b=True, which='major', axis='y')
plt.xlabel('Week')
plt.ylabel('Page Views')
plt.savefig('shp_pv.png')

# close
plt.close('all')

plt.figure()
df.iloc[0:14].plot(x='Week Starting', y=['Bounce Rate', 'PV Trend', 'Direct PV % of Site PV'], kind='line')
# plt.tight_layout()
plt.grid(b=True, which='major', axis='y')
plt.xlabel('Week')
plt.ylabel('Trends')
plt.savefig('shp_trend.png')

# close
plt.close('all')

plt.figure()
df.iloc[0:26].plot(x='Week Starting', y=['HP PV', 'Direct PV', 'Internal PV'], kind='line')
# plt.tight_layout()
plt.grid(b=True, which='major', axis='y')
plt.xlabel('Week')
plt.ylabel('Source PV')
plt.savefig('shp_bounce.png')

# close
plt.close('all')

df_tw = process_csv(tw_file_name, 'monthly')
df_tw['Month'] = pd.to_datetime(df_tw['Month'])

# df_tw.plot(x='Month', y=['Twitter Posts', 'Views'], kind='line')
# plt.grid(b=True, which='major', axis='y')
# plt.ylabel('PV Thousands')
# plt.savefig('tw_traffic.png')

ax = df_tw.plot(x="Month", y=["Tw posts", "Fb posts"], legend=False)
ax2 = ax.twinx()
df_tw.plot(x="Month", y=["Tw posts", "Fb posts"], ax=ax2, legend=False, color="r")
ax.figure.legend()
plt.savefig('tw_traffic.png')

# close
plt.close('all')

plt.figure()
df_tw.plot(x='Month', y=['Tw refs', 'Fb refs'], kind='line')
plt.grid(b=True, which='major', axis='y')
plt.xlabel('Month')
plt.ylabel('Page Views')
plt.savefig('social_traffic.png')

# close
plt.close('all')

