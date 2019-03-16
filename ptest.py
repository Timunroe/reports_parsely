import pandas as pd
import re
import pathlib
import sys
import utils_num_new as u


def t(n, min=None):
    # convert number to text for formatting
    if min:
        if n > min:
            return f'''**{re.sub('.0$','',str(n))}**'''
        else:
            return f'''<span style="color: red">**{re.sub('.0$','',str(n))}**</span>'''
    else:
        return re.sub('.0$', '', str(n))
    

# handy helpers
# print(list(df.columns.values))
newline = '\n'
dbline = '\n'

# FILES TO PROCESS
site_csv_test = "Spec-Site-Stats-Over-Time-14-weeks.csv"
articles_csv_test = 'Spec-top-posts-byMinutes-lastWeek.csv'

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
    s += f'''Limited to content with pubdate in last 2 days''' + newline
    for rank, item in enumerate(articles, start=1):
        # data for report
        visitors_total = u.humanize(item['Visitors'])
        print(str(visitors_total))
        min_per_visitor = round(item["Engaged minutes"] / item['Visitors'], 2)
        returning_vis = u.percentage(item['Returning vis.'], item['Visitors'])
        headline = item['Title'].title().replace('’T', '’t').replace('’S', '’s').replace("'S", "'s").replace('’M', '’m').replace('’R', '’r')
        author = item['Authors'].title().replace(' And', ',')
        section = item['Section'].replace('and you', '').replace('news|', '').title()
        source_social = u.percentage(item['Social refs'], item['Views'])
        fb = u.percentage(item['Fb refs'], item['Social refs'])
        tw = u.percentage(item['Tw refs'], item['Social refs'])
        buzz = u.humanize(item["Social interactions"])
        assetID = (re.search(r'.*(\d{7})-.*', item['URL'])).group(1)
        sources = [
            {'text': 'social', 'value': item['Social refs']}, 
            {'text': 'search', 'value': item['Search refs']}, 
            {'text': 'other', 'value': item['Other refs']},
            {'text': 'direct', 'value': item['Direct refs']},
            {'text': 'internal', 'value': item['Internal refs']},
        ]
        devices = [
            {'text': 'mobile', 'value': item['Mobile views']}, 
            {'text': 'desktop', 'value': item['Desktop views']}, 
            {'text': 'tablet', 'value': item['Tablet views']}, 
        ]
        # generate report
        s += f'''{rank}. {headline}''' + newline
        s += f'''By {author} in {section}'''
        s += f''' | {item['Publish date'][:-6]} | Asset# [{assetID}]({item['URL']})''' + newline
        s += f'''PV **{u.humanize(item['Views'])}** | visitors: **{visitors_total}**, {t(returning_vis)}% returning | {t(min_per_visitor, min=0.6)} min/visitor''' + newline
        # examine each stat, if < 10 don't bother showing it ...
        s += f'''key sources %: '''
        for x in sorted(sources, key=lambda k: k['value'], reverse=True):
            source_value = u.percentage(x['value'], item['Views'])
            if source_value > 15:
                s += f'''{x['text']} **{t(source_value)}**, '''
        s += newline
        # if social is < 10, don't include next line
        if source_social > 15:
            s += f'''social %: FB **{t(fb)}**'''
            if tw > 10:
                s += f''', Twitter **{t(tw)}**'''
            s += f''' | Interactions: {buzz}''' + newline
        s += f'''devices %: '''
        for x in sorted(devices, key=lambda k: k['value'], reverse=True):
            device_value = u.percentage(x['value'], item['Views'])
            if device_value > 10:
                s += f'''{x['text']} **{t(device_value)}**, '''
        s += newline
        s += f'---' + newline
    # return re.sub(', (<br>|</p>)', r'\1', s)
    return s
        


def top_article_by_referrer(articles, total, name, col_name):
    s = ''
    # s += "======================\n"
    s += f'''**{name.upper()}**: Top articles by page views''' + newline
    for item in articles:
        author = item['Authors'].title().replace(' And', ',')
        assetID = (re.search(r'.*(\d{7})-.*', item['URL'])).group(1)
        section = item['Section'].replace('and you', '').replace('news|', '').title()
        s += f'''{item['Title']}''' + newline
        s += f'''By {author} in {section}'''
        s += f''' | {item['Publish date'][:-6]} | Asset# [{assetID}]({item['URL']})''' + newline
        s += f'''**{t(u.percentage(item[col_name], total))}**% of total -- **{u.humanize(item[col_name])}** clicks''' + newline
        s += newline
    s += "======================<br>\n"
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
if len(sys.argv) > 2 and (sys.argv)[1] in ['daily', 'weekly', 'monthly'] and (sys.argv)[2] in ['spectator', 'record', 'niagara', 'standard', 'examiner', 'tribune', 'review', 'star']:
    freq = (sys.argv)[1]
    site = (sys.argv)[2]
else:
    print("Requires 2 parameters:\n[daily/weekly/monthly]\n[spectator/record/niagara/examiner/star]")
    sys.exit()


# ARTICLES STATS

df_article = process_csv(freq, site, articles_csv_test, article_cols_to_keep, True)
# TEST POINT
# print(df_article)
# print(df_article.dtypes)

# intialize string
report = '<head><meta charset="UTF-8"></head>'

# GET TOP ARTICLES BY MINUTES
# articles should be already sorted in CSV
# print(df_article.head(2).to_dict(orient='records'))
report += articles_stats(df_article.head(10).to_dict(orient='records'))

# GET TOP ARTICLES BY REFERRERS
referrers = [
    {'name': "Internal", 'col_name': 'Internal refs', 'limit': 3},
    {'name': "Search", 'col_name': 'Search refs', 'limit': 3},
    {'name': "Social", 'col_name': 'Social refs', 'limit': 3},
    {'name': "Other", 'col_name': 'Other refs', 'limit': 3},
    {'name': "Direct", 'col_name': 'Direct refs', 'limit': 3},
    {'name': "Facebook", 'col_name': 'Fb refs', 'limit': 3},
    {'name': "Twitter", 'col_name': 'Tw refs', 'limit': 3},
    {'name': "LinkedIn", 'col_name': 'Li refs', 'limit': 3}
]
report += '''===================================''' + newline
report += '''TOP POSTS: by Referrers''' + newline
report += '''-----------------------------------''' + newline
for item in referrers:
    articles = df_article.sort_values(by=[item['col_name']], ascending=False).head(
        item['limit']).to_dict(orient='records')
    total = df_article[item['col_name']].sum()

    report += top_article_by_referrer(articles,
                                      total, item['name'], item['col_name'])

# END ARTICLES STATS



print(report)
with open(f'data_reports/test.html', "w") as f:
    f.write(report)
