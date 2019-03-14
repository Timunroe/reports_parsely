import pandas as pd
import re
import utils_num as u

# handy helpers
# print(list(df.columns.values))
newline = '\n'

# FILES TO PROCESS
site_csv = "Spec-Site-Stats-14-weeks.csv"
article_csv = '/Users/timmunroe/Documents/PROJECTSLOCAL/reports_parsely/data_in/weekly/Spec-top-posts-byMinutes-lastWeek.csv'

# ==================
# ARTICLES
# ==================


def article_stats(articles):
    s = ''
    s += f'''===================================''' + newline
    s += f'''TOP POSTS: by Total Engaged Minutes''' + newline
    s += f'''Limited to content with pubdate in last 2 days''' + newline
    s += f'''-----------------------------------''' + newline
    for rank, item in enumerate(articles, start=1):
        tv = item['Visitors']
        tvu = item['Views']
        ts = item['Social refs']
        headline = item['Title'].title().replace('’T', '’t').replace('’S', '’s').replace("'S", "'s").replace('’M', '’m').replace('’R', '’r')
        author = item['Authors'].title().replace(' And', ',')
        section = item['Section'].replace('and you', '').replace('news|', '').title()
        assetID = (re.search(r'.*(\d{7})-.*', item['URL'])).group(1)
        s += f'''{rank}. {headline}''' + newline
        s += f'''By {author} in {section}'''
        s += f''' | {item['Publish date'][:-6]} | Asset# {assetID}''' + newline
        s += f'''VISITORS: {str(round(item["Engaged minutes"] / tv, 2))} min/visitor, visitors: {u.humanize(tv)}, returning: {u.percentage(item['Returning vis.'], tv)}''' + newline
        s += f'''TRAFFIC %: social {u.percentage(item['Social refs'], tvu)}, search {u.percentage(item['Search refs'], tvu)}, other {u.percentage(item['Other refs'], tvu)}, direct {u.percentage(item['Direct refs'], tvu)}, internal {u.percentage(item['Internal refs'], tvu)}''' + newline
        # if social is < 10, don't include next line
        s += f'''SOCIAL BREAKDOWN %: FB {u.percentage(item['Fb refs'], ts)}, Twitter {u.percentage(item['Tw refs'], ts)} | Interactions: {u.humanize(item["Social interactions"])}''' + newline
        s += f'''DEVICES %: mobile {u.percentage(item['Mobile views'], tvu)}, desktop {u.percentage(item['Desktop views'], tvu)}, tablet {u.percentage(item['Tablet views'], tvu)}''' + newline
        s += f'---------------------------' + newline
    return s


def top_article_by_referrer(articles, total, name, col_name):
    s = ''
    # s += "======================\n"
    s += f'{name.upper()}: Top articles by page views\n\n'
    for item in articles:
        s += f'''{item['Title']}''' + newline
        s += f'''By {item['Authors'].title().replace(' And', ',')} in {item['Section'].replace('and you', '').replace('news|', '').title()}'''
        assetID = (re.search(r'.*(\d{7})-.*', item['URL'])).group(1)
        s += f''' | {item['Publish date'][:-6]} | Asset# {assetID}''' + newline
        s += f'''{u.percentage(item[col_name], total)}% of total -- {u.humanize(item[col_name])} clicks''' + newline
        s += newline
    s += "======================\n"
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

df = pd.read_csv(article_csv,
                 usecols=article_cols_to_keep,
                 keep_default_na=False,
                 na_values='0')

df.columns = df.columns.str.replace('\xa0', ' ')
cols_to_fix = ["Search refs", "Internal refs", "Other refs", "Social refs", "Fb refs",
               "Tw refs", "Li refs", "Pi refs", "Social interactions", "Fb interactions", "Tw interactions"]
df[cols_to_fix] = df[cols_to_fix].apply(pd.to_numeric)

# intialize string
report = ''

# get top articles by minutes
# articles should be already sorted in CSV
report += article_stats(df.head(10).to_dict(orient='records'))

# get top articles by referrers
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
    articles = df.sort_values(by=[item['col_name']], ascending=False).head(
        item['limit']).to_dict(orient='records')
    total = df[item['col_name']].sum()

    report += top_article_by_referrer(articles,
                                      total, item['name'], item['col_name'])


print(report)

with open(f'data_reports/test.txt', "w") as f:
    f.write(report)
