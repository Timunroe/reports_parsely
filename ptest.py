import pandas as pd
import markdown
import re
import pathlib
import sys
import utils_num_new as u

# requires  stats over time by ALL PAGES report.

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
    s += f'''### TOP POSTS: by Total Engaged Minutes''' + newline
    s += f'''###### Limited to content with pubdate in last 2 days''' + newline
    for rank, item in enumerate(articles, start=1):
        # data for report
        visitors_total = u.humanize(item['Visitors'])
        # print(str(visitors_total))
        headline = item['Title'].title().replace('’T', '’t').replace('’S', '’s').replace("'S", "'s")\
            .replace('’M', '’m').replace('’R', '’r')
        author = item['Authors'].title().replace(' And', ',')
        section = item['Section'].replace('and you', '').replace('news|', '').title()
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
        s += f''' | {item['Publish date'][:-6]} | Asset# [{assetID}]({item['URL']})''' + newline
        s += f'''PV **{u.humanize(item['Views'])}** | visitors: **{visitors_total}**, '''
        s += f'''{t(item['Returning%'])}% returning | {t(item['time'], mn=0.6)} min/visitor''' + newline
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
        author = item['Authors'].title().replace(' And', ',')
        assetID = (re.search(r'.*(\d{7})-.*', item['URL'])).group(1)
        section = item['Section'].replace('and you', '').replace('news|', '').title()
        s += f'''{item['Title']}''' + newline
        # s += f'''By {author} in {section}'''
        # s += f''' | {item['Publish date'][:-6]} | Asset# [{assetID}]({item['URL']})''' + newline
        s += f'''**{t(u.percentage(item[col_name], total))}**% of total -- **{u.humanize(item[col_name])}** clicks'''
        s += f''' | asset [{assetID}]({item['URL']})''' + newline
        s += newline
    s += "---\n"
    return s


# FIX CSV FILE
article_cols_to_keep = [
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
site_cols_to_keep = [
    'Date',
    'Visitors (all pages)',
    'Visitors (posts)',
    'Views (all pages)',
    'Views (posts)',
    'Desktop views',
    'Mobile views',
    'Tablet views',
    'Engaged Minutes (all pages)',
    'Engaged Minutes (posts)',
    'New Posts',
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


def process_csv(freq, site, file_name, cols_to_keep=None, parsely_fix=True):
    if parsely_fix:
        path = pathlib.Path.cwd() / 'data_in' / f'{freq}' / file_name
        fixed_csv = path.read_text().replace('.0', '').replace('\xa0', ' ').replace(',,,,', ',0,0,0,').replace(',,,', ',0,0,').replace(',,', ',0,').replace(',\n', ',0\n')
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
    print("Requires 2 parameters:\n[daily/weekly/monthly]\n[spectator/record/niagara/examiner/star]")
    sys.exit()

# FILES TO PROCESS
if site == 'spectator':
    site_csv = "Spec-Site-Stats-14-weeks-pages.csv"
    articles_csv = 'Spec-top-posts-byMinutes-lastWeek.csv'
elif site == 'record':
    site_csv = "Rec-Site-Stats-Over-Time.csv"
    articles_csv = 'Rec-top-posts-byMinutes-lastWeek.csv'
elif site == 'standard':
    site_csv = "Standard-Site-Stats-14-weeks-pages.csv"
    articles_csv = 'Standard-top-posts-byMinutes-lastWeek.csv'

# intialize string
report = ''

# SITE STATS
site_cols_to_keep = [
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

df_site = process_csv(freq, site, site_csv, site_cols_to_keep, True)

# Add columns of calculations we'll need
df_site['Social%'] = round((df_site['Social refs'] / df_site['Views']) * 100, 0)
df_site['Search%'] = round((df_site['Search refs'] / df_site['Views']) * 100, 0)
df_site['Other%'] = round((df_site['Other refs'] / df_site['Views']) * 100, 0)
df_site['Direct%'] = round((df_site['Direct refs'] / df_site['Views']) * 100, 0)
df_site['Internal%'] = round((df_site['Internal refs'] / df_site['Views']) * 100, 0)
df_site['Fb%'] = round((df_site['Fb refs'] / df_site['Views']) * 100, 0)
df_site['Tw%'] = round((df_site['Tw refs'] / df_site['Views']) * 100, 0)
df_site['Mobile%'] = round((df_site['Mobile views'] / df_site['Views']) * 100, 0)
df_site['Desktop%'] = round((df_site['Desktop views'] / df_site['Views']) * 100, 0)
df_site['Tablet%'] = round((df_site['Tablet views'] / df_site['Views']) * 100, 0)
df_site['time'] = round((df_site['Engaged minutes'] / df_site['Views']), 2)
df_site['Returning%'] = round((df_site['Returning vis.'] / df_site['Views']) * 100, 0)
# this period data = df_site.head(1)
# rolling average data = df_site.tail(len(df_site.index) - 1)
# print(df_site)

pv = df_site.head(1)['Views'].item()
pv_vs_ma = u.vs_ma(df_site.head(1)['Views'].item(), df_site.tail(len(df_site.index) - 1)['Views'].mean())
v = df_site.head(1)['Visitors'].item()
v_vs_ma = u.vs_ma(df_site.head(1)['Visitors'].item(), df_site.tail(len(df_site.index) - 1)['Visitors'].mean())
m = df_site.head(1)['Engaged minutes'].item()
m_vs_ma = u.vs_ma(df_site.head(1)['Engaged minutes'].item(), df_site.tail(len(df_site.index) - 1)['Engaged minutes'].mean())
fb_delta = df_site.head(1)['Fb refs'].item() - df_site.tail(len(df_site.index) - 1)['Fb refs'].mean()
tw_delta = df_site.head(1)['Tw refs'].item() - df_site.tail(len(df_site.index) - 1)['Tw refs'].mean()
other_delta = df_site.head(1)['Other refs'].item() - df_site.tail(len(df_site.index) - 1)['Other refs'].mean()
search_delta = df_site.head(1)['Search refs'].item() - df_site.tail(len(df_site.index) - 1)['Search refs'].mean()
direct_delta = df_site.head(1)['Direct refs'].item() - df_site.tail(len(df_site.index) - 1)['Direct refs'].mean()
internal_delta = df_site.head(1)['Internal refs'].item() - df_site.tail(len(df_site.index) - 1)['Internal refs'].mean()
mobile = df_site.head(1)['Mobile%'].item()
desktop = df_site.head(1)['Desktop%'].item()
tablet = df_site.head(1)['Tablet%'].item()
shifts = [
    {'text': 'FB', 'value': fb_delta},
    {'text': 'Tw', 'value': tw_delta},
    {'text': 'Search', 'value': search_delta},
    {'text': 'Other', 'value': other_delta},
    {'text': 'Direct', 'value': direct_delta},
    {'text': 'Internal', 'value': internal_delta},
]
report += f'''\n## Weekly report {site.title()}\n'''
report += f'''### HIGHLIGHTS:\n'''
report += f'''Page views: {u.humanize(pv)}, **{pv_vs_ma:+}%** vs average.\n'''
report += f'''Changes: '''
for x in sorted(shifts, key=lambda k: k['value'], reverse=True):
    if abs(x['value']) > 500:
        report += f'''{x['text']} **{u.humanize(x['value'])}**, '''
report += '\n'
report += f'''Visitors: {u.humanize(v)}, **{v_vs_ma:+}%** vs average.\n'''
report += f'''Minutes: {u.humanize(m)}, **{m_vs_ma:+}%** vs average.\n'''
report += f'''Devices %: {mobile} mobile, {desktop} desktop, {tablet} tablet\n\n'''
# END SITE STATS

# ARTICLES STATS
df_article = process_csv(freq, site, articles_csv, article_cols_to_keep, True)
# TEST POINT
# print(df_article)
# print(df_article.dtypes)
# Add columns of calculations we'll need
df_article['Social%'] = round((df_article['Social refs'] / df_article['Views']) * 100, 0)
df_article['Search%'] = round((df_article['Search refs'] / df_article['Views']) * 100, 0)
df_article['Other%'] = round((df_article['Other refs'] / df_article['Views']) * 100, 0)
df_article['Direct%'] = round((df_article['Direct refs'] / df_article['Views']) * 100, 0)
df_article['Internal%'] = round((df_article['Internal refs'] / df_article['Views']) * 100, 0)
df_article['Fb%'] = round((df_article['Fb refs'] / df_article['Views']) * 100, 0)
df_article['Tw%'] = round((df_article['Tw refs'] / df_article['Views']) * 100, 0)
df_article['Mobile%'] = round((df_article['Mobile views'] / df_article['Views']) * 100, 0)
df_article['Desktop%'] = round((df_article['Desktop views'] / df_article['Views']) * 100, 0)
df_article['Tablet%'] = round((df_article['Tablet views'] / df_article['Views']) * 100, 0)
df_article['time'] = round((df_article['Engaged minutes'] / df_article['Visitors']), 2)
df_article['Returning%'] = round((df_article['Returning vis.'] / df_article['Visitors']) * 100, 0)

article_cols_to_keep = [
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

# GET TOP ARTICLES BY MINUTES
# articles should be already sorted in CSV
# TEST POINT
# print(df_article.head(2).to_dict(orient='records'))
report += articles_stats(df_article.head(10).to_dict(orient='records'))

# GET TOP ARTICLES BY REFERRERS
referrers = [
    {'name': "Search", 'col_name': 'Search refs', 'limit': 3},
    {'name': "Other", 'col_name': 'Other refs', 'limit': 3},
    {'name': "Social", 'col_name': 'Social refs', 'limit': 3},
    {'name': "Facebook", 'col_name': 'Fb refs', 'limit': 3},
    {'name': "Twitter", 'col_name': 'Tw refs', 'limit': 3},
    {'name': "LinkedIn", 'col_name': 'Li refs', 'limit': 3},
    {'name': "Internal", 'col_name': 'Internal refs', 'limit': 3},

    # {'name': "Direct", 'col_name': 'Direct refs', 'limit': 3},
]
report += '''---''' + newline
report += '''### **TOP POSTS**: by Referrers''' + newline
for item in referrers:
    articles = df_article.sort_values(by=[item['col_name']], ascending=False).head(
        item['limit']).to_dict(orient='records')
    total = df_article[item['col_name']].sum()
    report += top_article_by_referrer(articles, total, item['name'], item['col_name'])

# END ARTICLES STATS
print(report)
# print(len(df_site.index))
# print(df_site.dtypes)
head = '''<html><head><meta charset="UTF-8"><style>html{font-family:sans-serif;line-height:1.15;\
-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;-ms-overflow-style:scrollbar;\
-webkit-tap-highlight-color:transparent}@-ms-viewport{width:device-width}\
article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}\
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;\
font-size:1rem;font-weight:400;line-height:1.5;color:#212529;text-align:left;\
background-color:#fff}h1,h2,h3,h4,h5,h6{margin-top:0;margin-bottom:16px;}p{margin-top:0;margin-bottom:16px;}\
dl,ol,ul{margin-top:0;margin-bottom:14px;}li{margin-bottom:16px;}\
table{display:table;border-collapse:collapse;border-spacing:0;width:100%;}th{text-align: inherit;}p{}</style></head><body>\
'''
tail = '</body></html>'

html = markdown.markdown(re.sub(', \n', '\n', report.replace('.0', '')), extensions=['extra', 'nl2br'])
report = head + html + tail

with open(f'data_reports/test.html', "w") as f:
    f.write(report)
