import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import markdown
import pathlib
import sys
import re
import utils_num_new as u

sns.set()
rcParams.update({'figure.autolayout': True})
# close
plt.close('all')

# STREAMLINING ... 2 files, posts and site,
# that go back far enough (6 months) for rolling means
# Do as much calculation in Pandas before converting to dicts for report format
# normalize any differences in reports (ie Engaged Minutes vs Engaged minutes)

# Columns in posts CSV
'''
URL	Title,Publish date,Authors,Section Tags,Sort (Engaged minutes),Visitors,Views,
Engaged minutes,New vis.,Returning vis.,Views new vis.,Avg. views new vis.,
Views ret. vis.,Avg. views ret. vis.,Minutes New Vis.,Avg. minutes new vis.,
Minutes Ret. Vis.,Avg. minutes ret. vis.,Desktop views,Mobile views,Tablet views
Search refs,Internal refs,Other refs,Direct refs,Social refs,Fb refs,Tw refs,Li refs,Pi refs,
Social interactions,Fb interactions,Tw interactions,Li interactions,Pi interactions
Video starts,Video minutes watched,Website views,AMP views,Fb instant views,Post id
'''
# Columns in site CSV
'''
Date,Posts,New Posts,Visitors,Views,Engaged minutes,Social interactions
Fb interactions,Tw interactions,Li interactions,Pi interactions
Desktop views,Mobile views,Tablet views,Search refs,Internal refs
Other refs,Direct refs,Social refs,Fb refs,Tw refs,Li refs,Pi refs
Channel vis.,New vis.,Views new vis.,Avg. views new vis.,Minutes New Vis.
Avg. minutes new vis.,Returning vis.,Views ret. vis.,Avg. views ret. vis.,Minutes Ret. Vis.
Avg. minutes ret. vis.,Website views,AMP views,Fb instant views
'''


def t(n, mn=None, sign=False):
    # convert number to text for formatting
    if sign:
        if n > 0:
            symbol = '+'
        else:
            symbol = ''
    else:
        symbol = ''
    if mn:
        if n > mn:
            return f'''**{re.sub('.0$', '', symbol + str(n))}**'''
        else:
            return f'''<span style="color: red">**{re.sub('.0$', '', symbol + str(n))}**</span>'''
    else:
        return re.sub('.0$', '', symbol + str(n))


def sign(text):
    if not text.startswith('-'):
        text = '+' + text
    # convert number to text with plus/minus sign
    return text


# handy helpers
# print(list(df.columns.values))
newline = '\n'
dbline = '\n\n'

# ==================
# ARTICLES
# ==================

# HOW DO WE PRESENT SOURCES, SOCIAL, DEVICES
# in order from largest to smallest?
# make each one a dict with a key of value, then sort by that?
# there would also have to be a key of text to print


def articles_stats(articles):
    # articles is a dict as converted from pandas dataframe
    s = ''
    s += f'''\n### TOP POSTS: by Total Engaged Minutes''' + newline
    # s += f'''###### Limited to content with pubdate in last 2 days''' + newline
    for rank, item in enumerate(articles, start=1):
        # data for report
        visitors_total = u.humanize(item['Visitors'])
        # print(str(visitors_total))
        headline = item['Title'].title().replace('’T', '’t')\
            .replace('’S', '’s').replace("'S", "'s")\
            .replace('’M', '’m').replace('’R', '’r')
        author = item['Authors'].title().replace(' And', ',')
        section = item['Section'].replace(
            'and you', '').replace('news|', '').title()
        buzz = u.humanize(item["Social interactions"])
        assetID = (re.search(r'.*(\d{7})-.*', item['URL'])).group(1)
        sources = [
            {'text': 'FB', 'value': item['Fb%']},
            {'text': 'Tw', 'value': item['Tw%']},
            {'text': 'search', 'value': item['Search%']},
            {'text': 'other', 'value': item['Other%']},
            {'text': 'direct', 'value': item['Direct%']},
            {'text': 'internal', 'value': item['Internal%']},
        ]
        devices = [
            {'text': 'mobile', 'value': item['Mobile%']},
            {'text': 'desktop', 'value': item['Desktop%']},
            {'text': 'tablet', 'value': item['Tablet%']},
        ]
        # generate report
        s += f'''{rank}. {headline}''' + newline
        s += f'''By {author} in {section}'''
        s += f''' | {item['Publish date'].date()} | '''
        s += f'''Asset# [{assetID}]({item['URL']})''' + newline
        s += f'''PV **{u.humanize(item['Views'])}** | visitors: **{visitors_total}**, '''
        s += f'''{t(item['Returning%'])}% returning | {t(item['time'], mn=0.6)} min/visitor'''
        s += newline
        # examine each stat, if < 10 don't bother showing it ...
        s += f'''Key sources %: '''
        for x in sorted(sources, key=lambda k: k['value'], reverse=True):
            if x['value'] > 10:
                s += f'''{x['text']} **{t(x['value'])}**, '''
        s += newline
        s += f'''Devices %: '''
        for x in sorted(devices, key=lambda k: k['value'], reverse=True):
            if x['value'] > 10:
                s += f'''{x['text']} **{t(x['value'])}**, '''
        s += newline
        s += f'''Social interactions: {buzz}''' + newline
    return s


def top_article_by_referrer(articles, total, name, col_name):
    s = ''
    # s += "======================\n"
    s += f'''#### **{name.upper()}**: Top articles by page views''' + newline
    for item in articles:
        # author = item['Authors'].title().replace(' And', ',')
        assetID = (re.search(r'.*(\d{7})-.*', item['URL'])).group(1)
        # section = item['Section']\
        # .replace('and you', '').replace('news|', '').title()
        s += f'''{item['Title']}''' + newline
        # s += f'''By {author} in {section}'''
        # s += f''' | {item['Publish date'][:-6]} | Asset# [{assetID}]({item['URL']})''' + newline
        if col_name == 'Social interactions':
            s += f'''**{t(u.percentage(item[col_name], total))}**% of total -- **{u.humanize(item[col_name])}** interactions'''
        else:
            s += f'''**{t(u.percentage(item[col_name], total))}**% of total -- **{u.humanize(item[col_name])}** clicks'''
        s += f''' | asset [{assetID}]({item['URL']})''' + newline
        s += newline
    if name == 'Other':
        s += f'''##### Usually Google News, but could be another curator like Flipboard.\n\n'''
    s += "---\n"
    return s


# FIX CSV FILE
posts_cols_keep = [
    'URL', 'Title', 'Publish date', 'Authors', 'Section', 'Visitors', 'Views',
    'Engaged minutes', 'New vis.', 'Returning vis.', 'Desktop views',
    'Mobile views', 'Tablet views', 'Search refs', 'Internal refs',
    'Other refs', 'Direct refs', 'Social refs', 'Fb refs', 'Tw refs',
    'Li refs', 'Social interactions', 'Fb interactions',
    'Tw interactions', 'Li refs'
]


def process_csv(freq, site, file_name, cols_to_keep=None, parsely_fix=True):
    if parsely_fix:
        path = pathlib.Path.cwd() / 'data_in' / f'{freq}' / file_name
        fixed_csv = path.read_text().replace('.0', '').replace('\xa0', ' ')\
            .replace(',,,,', ',0,0,0,').replace(',,,', ',0,0,')\
            .replace(',,', ',0,').replace(',\n', ',0\n')
        # TEST POINT
        # print(fixed_csv)
    if cols_to_keep:
        df = pd.read_csv(pd.compat.StringIO(fixed_csv), usecols=cols_to_keep)
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


# MAIN
if len(sys.argv) > 2 and (sys.argv)[1] in ['daily', 'weekly', 'monthly'] and (sys.argv)[2] \
        in ['spectator', 'record', 'niagara', 'standard', 'examiner', 'tribune', 'review', 'star']:
    freq = (sys.argv)[1]
    site = (sys.argv)[2]
else:
    print(
        "Requires 2 parameters:\n[daily/weekly/monthly]\n[spectator/record/niagara/examiner/star]")
    sys.exit()

# FILES TO PROCESS
site_csv = f'''{site}_site.csv'''
pages_csv = f'''{site}_pages.csv'''

# intialize string
report = ''

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
    'Li interactions',
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
    'Li refs',
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

df = process_csv(freq, site, site_csv, site_cols_keep, True)
df['Date'] = pd.to_datetime(df['Date'])
# reverse sort on Date because that's how Pandas likes to roll
df_site = df.sort_values(by=['Date'])

# Add columns of calculations we'll need
# rolling means
if freq == 'weekly':
    r_units = 13
if freq == 'daily':
    r_units = 90
if freq == 'monthly':
    r_units = 3

df_site['Views rm'] = df_site['Views'].rolling(window=r_units, center=False).mean()
# print(df_site.tail(1))
# print(df_site[['Views','Views rm']])


df_site['Visitors rm'] = df_site['Visitors'].rolling(
    window=r_units, center=False).mean()
df_site['Minutes rm'] = df_site['Engaged minutes'].rolling(
    window=r_units, center=False).mean()
df_site['Fb rm'] = df_site['Fb refs'].rolling(window=r_units, center=False).mean()
df_site['Tw rm'] = df_site['Tw refs'].rolling(window=r_units, center=False).mean()
df_site['Search rm'] = df_site['Search refs'].rolling(
    window=r_units, center=False).mean()
df_site['Other rm'] = df_site['Other refs'].rolling(
    window=r_units, center=False).mean()
df_site['Direct rm'] = df_site['Direct refs'].rolling(
    window=r_units, center=False).mean()
df_site['Internal rm'] = df_site['Internal refs'].rolling(
    window=r_units, center=False).mean()

# Percentages
df_site['Social%'] = round(
    (df_site['Social refs'] / df_site['Views']) * 100, 0)
df_site['Search%'] = round(
    (df_site['Search refs'] / df_site['Views']) * 100, 0)
df_site['Other%'] = round((df_site['Other refs'] / df_site['Views']) * 100, 0)
df_site['Direct%'] = round(
    (df_site['Direct refs'] / df_site['Views']) * 100, 0)
df_site['Internal%'] = round(
    (df_site['Internal refs'] / df_site['Views']) * 100, 0)
df_site['Fb%'] = round((df_site['Fb refs'] / df_site['Views']) * 100, 0)
df_site['Tw%'] = round((df_site['Tw refs'] / df_site['Views']) * 100, 0)
df_site['Mobile%'] = round(
    (df_site['Mobile views'] / df_site['Views']) * 100, 0)
df_site['Desktop%'] = round(
    (df_site['Desktop views'] / df_site['Views']) * 100, 0)
df_site['Tablet%'] = round(
    (df_site['Tablet views'] / df_site['Views']) * 100, 0)
df_site['Returning%'] = round(
    (df_site['Returning vis.'] / df_site['Views']) * 100, 0)
# Minutes per visitor
df_site['time'] = round((df_site['Engaged minutes'] / df_site['Views']), 2)

# this period data = df_site.head(1)
# rolling average data = df_site.tail(len(df_site.index) - 1)
# print(df_site)

# Actual data needed in text report
pv = df_site.tail(1)['Views'].item()
pv_vs_ra = round(
    ((pv - df_site.tail(1)['Views rm'].item()) / df_site.tail(1)['Views rm'].item()) * 100, 0)
v = df_site.tail(1)['Visitors'].item()
v_vs_ra = round(
    ((v - df_site.tail(1)['Visitors rm'].item()) / df_site.tail(1)['Visitors rm'].item()) * 100, 0)
m = df_site.tail(1)['Engaged minutes'].item()
m_vs_ra = round(
    ((m - df_site.tail(1)['Minutes rm'].item()) / df_site.tail(1)['Minutes rm'].item()) * 100, 0)
fb_delta = df_site.tail(1)['Fb refs'].item() - df_site.tail(1)['Fb rm'].item()
tw_delta = df_site.tail(1)['Tw refs'].item() - df_site.tail(1)['Tw rm'].item()
other_delta = df_site.tail(1)['Other refs'].item() - \
    df_site.tail(1)['Other rm'].item()
search_delta = df_site.tail(1)['Search refs'].item(
) - df_site.tail(1)['Search rm'].item()
direct_delta = df_site.tail(1)['Direct refs'].item(
) - df_site.tail(1)['Direct rm'].item()
internal_delta = df_site.tail(1)['Internal refs'].item(
) - df_site.tail(1)['Internal rm'].item()
mobile = df_site.tail(1)['Mobile%'].item()
desktop = df_site.tail(1)['Desktop%'].item()
tablet = df_site.tail(1)['Tablet%'].item()
shifts = [
    {'text': 'FB', 'value': fb_delta},
    {'text': 'Tw', 'value': tw_delta},
    {'text': 'Search', 'value': search_delta},
    {'text': 'Other', 'value': other_delta},
    {'text': 'Direct', 'value': direct_delta},
    {'text': 'Internal', 'value': internal_delta},
]
report += f'''\n## {freq.title()} report {site.title()}\n'''
report += f'''### SITE HIGHLIGHTS:\n'''
# need test here: if pv number 6 digits, fraction point = 0, but if 7, fraction point = 2
report += f'''Page views: {u.humanize(pv, 2) if pv > 1000000 else u.humanize(pv, 0)}, **{pv_vs_ra:+}%** vs average.\n'''
report += f'''Breakdown %: {df_site.tail(1)['Social%'].item():.0f} social, '''
report += f'''{df_site.tail(1)['Search%'].item():.0f} search, '''
report += f'''{df_site.tail(1)['Internal%'].item():.0f} internal, '''
report += f'''{df_site.tail(1)['Direct%'].item():.0f} direct, '''
report += f'''{df_site.tail(1)['Other%'].item():.0f} other\n'''
report += f'''Devices %: {mobile:.0f} mobile, {desktop:.0f} desktop, '''
report += f'''{tablet:.0f} tablet\n\n'''
report += f'''Referral changes vs average: '''
for x in sorted(shifts, key=lambda k: k['value'], reverse=True):
    if abs(x['value']) > 999:
        report += f'''{x['text']} **{u.humanize(x['value'])}**, '''
report += '\n\n'
report += f'''Visitors: {u.humanize(v, 2) if v > 1000000 else u.humanize(v, 0)}, **{v_vs_ra:+}%** vs average.\n'''
report += f'''Minutes: {u.humanize(m, 2) if m > 1000000 else u.humanize(m, 0)}, **{m_vs_ra:+}%** vs average.\n'''
if freq == 'weekly':
    report += f'''##### *Average is 13-week rolling mean.'''
if freq == 'daily':
    report += f'''##### *Average is 90-day rolling mean.'''
if freq == 'monthly':
    report += f'''##### *Average is 3-month rolling mean.'''
# TEST POINT
# print(report)

# PLOT rolling averages of key metrics
plt.figure()
# df_site.plot(x='Date', y=['Tw rm', 'Fb rm'], kind='line')
df_site[df_site['Views rm'].notnull()].plot(x='Date', y=['Views rm', 'Minutes rm', 'Tw rm', 'Fb rm'], kind='line')
# plt.tight_layout()
plt.grid(b=True, which='major', axis='y')
# plt.xlabel('Weeks')
if freq == 'monthly':
    plt.ylabel('3-month rolling means')
if freq == 'weekly':
    plt.ylabel('13-week rolling means')
if freq == 'daily':
    plt.ylabel('90-day rolling means')
plt.legend(loc='upper left')
plt.savefig('data_out/s_weekly_ra.png')

# close
plt.close('all')

# END SITE STATS

# ARTICLES STATS
pages_cols_keep = [
    'URL',
    'Title',
    'Publish date',
    'Authors',
    'Section',
    'Visitors',
    'Views',
    'Engaged minutes',
    'New vis.',
    'Returning vis.',
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
    'Li refs',
    'Pi refs',
    'Social interactions',
    'Fb interactions',
    'Tw interactions',
]

df = process_csv(freq, site, pages_csv, pages_cols_keep, True)
# filter out non articles, convert pub date to time object
df_article = df.copy()
# df_article = df_article[df_article['URL'].str.contains('story')]
# Need to filter out stray records with empty timestamp.
df_article = df_article[(df_article['URL'].str.contains('story')) & (df_article['Publish date'] != '0')]
# print(df_article['Publish date'].tail(5))
df_article['Publish date'] = pd.to_datetime(df_article['Publish date'])

# TEST POINT
# print(df_article)
# print(df_article.dtypes)
# Add columns of calculated percentages
for x in [('Social%', 'Social refs'), ('Search%', 'Search refs'),
          ('Other%', 'Other refs'), ('Direct%', 'Direct refs'),
          ('Internal%', 'Internal refs'),
          ('Fb%', 'Fb refs'), ('Tw%', 'Tw refs'), ('Mobile%', 'Mobile views'),
          ('Desktop%', 'Desktop views'), ('Tablet%', 'Tablet views')]:
    df_article[x[0]] = round((df_article[x[1]] / df_article['Views']) * 100, 0)

df_article['time'] = round(
    (df_article['Engaged minutes'] / df_article['Visitors']), 2)
df_article['Returning%'] = round(
    (df_article['Returning vis.'] / df_article['Visitors']) * 100, 0)

# GET TOP ARTICLES BY MINUTES
# articles should be already sorted in CSV
# TEST POINT
# print(df_article.head(2).to_dict(orient='records'))
report += articles_stats(df_article.head(10).to_dict(orient='records'))

# GET TOP ARTICLES BY REFERRERS
referrers = [
    {'name': "Internal", 'col_name': 'Internal refs', 'limit': 3},
    {'name': "Search", 'col_name': 'Search refs', 'limit': 3},
    {'name': "Other", 'col_name': 'Other refs', 'limit': 3},
    {'name': "Social interactions", 'col_name': 'Social interactions', 'limit': 3},
    {'name': "Social", 'col_name': 'Social refs', 'limit': 3},
    {'name': "Facebook", 'col_name': 'Fb refs', 'limit': 3},
    {'name': "Twitter", 'col_name': 'Tw refs', 'limit': 3},
    {'name': "LinkedIn", 'col_name': 'Li refs', 'limit': 3},
    # {'name': "Direct", 'col_name': 'Direct refs', 'limit': 3},
]
report += '''---''' + newline
report += '''### **TOP POSTS**: by Referrers''' + newline
for item in referrers:
    articles = df_article.sort_values(by=[item['col_name']], ascending=False).head(
        item['limit']).to_dict(orient='records')
    total = df_article[item['col_name']].sum()
    report += top_article_by_referrer(articles,
                                      total, item['name'], item['col_name'])

# END ARTICLES STATS
print(report)
# print(len(df_site.index))
# print(df_site.dtypes)
head = '''<html><head><meta charset="UTF-8"><style>\
html{font-family:sans-serif;line-height:1.15;\
-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;-ms-overflow-style:scrollbar;\
-webkit-tap-highlight-color:transparent}\
article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}\
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,\
"Helvetica Neue",Arial,sans-serif;\
font-size:1rem;font-weight:400;line-height:1.5;color:#212529;text-align:left;\
background-color:#fff}h1,h2,h3,h4,h5,h6{margin-top:0;margin-bottom:16px;}\
p{margin-top:0;margin-bottom:16px;}\
dl,ol,ul{margin-top:0;margin-bottom:14px;}li{margin-bottom:16px;}\
table{display:table;border-collapse:collapse;border-spacing:0;width:100%;}\
th{text-align: inherit;}p{}</style></head><body>\
'''
tail = '</body></html>'

html = markdown.markdown(re.sub(', \n', '\n', report), extensions=['extra', 'nl2br'])
report = head + html + tail

with open(f'data_reports/test.html', "w") as f:
    f.write(report)
