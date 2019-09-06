import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
from io import StringIO
import pathlib
import sys
import re
import utils_num_new as u

sns.set()
rcParams.update({'figure.autolayout': True})
# close
plt.close('all')


def process_csv(filename, folders=None, cols_to_keep=None):
    if folders:
        if not isinstance(folders, list):
            print("Folders paramaeter MUST be a list!")
            sys.exit()
        p = pathlib.Path.cwd().joinpath(*folders)
    else:
        p = pathlib.Path.cwd()
    path = p.joinpath(filename)
    csv_data = path.read_text()
    '''
    .replace('.0', '')\
        .replace('\xa0', ' ')\
        .replace(',,,,', ',0,0,0,').replace(',,,', ',0,0,')\
        .replace(',,', ',0,').replace(',\n', ',0\n')
    '''
    # TEST POINT
    # print(fixed_csv)
    if cols_to_keep:
        df = pd.read_csv(StringIO(csv_data), usecols=cols_to_keep)
    else:
        df = pd.read_csv(StringIO(csv_data))
    return df


'''
# domain_id,
# article_id,
article_create_date,
article_url,
article_title,
article_authors,
article_sections,
article_topics,
# article_subs_type,
article_pid,
article_word_count,
# articles_number,
article_reads,
attention_minutes,
attention_minutes_average,
social_actions,
read_depth,
# page_depth,
article_reads_average,
# social_actions_average,
# rows_total,
# cpi_general,
# cpi_exposure,
# cpi_engagement,
# cpi_loyalty,
# cpi_exposure_marker,
# cpi_engagement_marker,
# cpi_loyalty_marker,
# cpi_perspective

'''

# MAIN START

avg_reading_per_minute = 200
# file_name = 'CI_spec_feb_july_edit.csv'
file_name = 'CI_spec_local_sept2018_Aug2019.csv'

df = process_csv(file_name, ['data_in', 'readdepth'])

# DROP UNUSED COLUMNS
df = df.drop(
    ["domain_id", "article_id", "article_subs_type",
     "articles_number", "social_actions_average", "rows_total",
     "cpi_general", "cpi_exposure", "cpi_engagement", "cpi_loyalty", "cpi_exposure_marker",
     "cpi_engagement_marker", "cpi_loyalty_marker", "cpi_perspective", ], axis=1)

# ADD NEEDED COLUMNS
df['words_read'] = (df['attention_minutes_average'] / 60) * avg_reading_per_minute
df['percent_read'] = 100 * (df['words_read'] / df['article_word_count'])

articles_all = df[df['article_word_count'] > 0]
articles_localnews = df[ (df['article_word_count'] > 0) & (df['article_sections'].str.contains('news>local'))]
articles_total = articles_localnews['article_word_count'].count()

print('Articles total: ', articles_total)

data = []
count_list = [
    (0, 100),
    (100, 200), (200, 300), (300, 400), (400, 500), (500, 600),
    (600, 700), (700, 800), (800, 900), (900, 1000), (1000, 1100),
    (1100, 1200), (1200, 1300), (1300, 1400), (1400, 1500), (1500, 1600),
    (1600, 1700), (1700, 1800), (1800, 1900), (1900, 2000), (2000, 2500),
    (2500, 3000), (3000, 4000), (4000, 5000), (5000, 10000)
]

for i in count_list:
    # range_name = f'''{str(i[0])}'''
    tmp = {}
    tmp['wc'] = f'''{str(i[0]+1)}-{str(i[1])}'''
    bob = df[(df['article_word_count'] > (i[0]))
             & (df['article_word_count'] < (i[1] + 1))
             & (df['article_sections'].str.contains('news>local'))
             ]
    tmp['article_total'] = bob['article_word_count'].count()
    tmp['pc_articles_total'] = f'''{(100*(tmp['article_total'] / articles_total)):.2f}'''
    tmp['avg_time_spent'] = bob['attention_minutes_average'].mean()
    tmp['increase_words_written'] = f'''{((((i[1] + 50) - (i[0] + 50)) / (i[0]+50)) * 100):.0f}'''
    tmp['read_depth_avg'] = bob['read_depth'].mean()
    tmp['words_read'] = (tmp['avg_time_spent'] / 60) * avg_reading_per_minute
    tmp['avg_%_article_read'] = bob['percent_read'].mean()

    data.append(tmp)

print('====================================================================')
print('           |      PRODUCTION       |      TIME SPENT      | READ DEPTH')
print('--------------------------------------------------------------------')
print('Word count | Articles | % of total | Avg Sec | + Words | Avg % Read | Avg. Read Depth')
print('--------------------------------------------------------------------')
tc = 0
for i in data:
    # the_string = f'''{round(i['avg_%_article_read'], 0)}'''
    the_string = f'''{str(i['wc']).rjust(10)} | {str(i['article_total']).rjust(8)} | {str(i['pc_articles_total']).rjust(10)} | '''
    the_string += f'''{(i['avg_time_spent']):7.0f} | {(i['increase_words_written']).rjust(6)} | {(i['avg_%_article_read']):6.0f}'''
    the_string += f'''{(i['read_depth_avg']):6.1f}    '''
    print(the_string)
    tc += i['article_total']
print('--------------------------------------------------------------------')
print('Total articles: ', tc)
