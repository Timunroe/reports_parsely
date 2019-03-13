import pandas as pd
import utils_num as u

file_name = "reports/monthly/Spec-top-posts-byMinute-lastMonth-thespec-com-Website-post.csv"
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


def article_stats(data, kind=None, total=None):
    s = ''
    newline = '\n'
    for item in data:
        tv = item['Visitors']
        tvu = item['Views']
        ts = item['Social refs']
        s += f'''{item['Title']}''' + newline
        s += f'''By {item['Authors'].title()} in {item['Section'].replace('and you', '')} | {item['Publish date'][:-6]}''' + newline
        s += f'''VISITORS: {str(round(item["Engaged minutes"] / tv, 2))} min/visitor, visitors: {u.humanize(tv)}, returning: {u.percentage(item['Returning vis.'], tv)}''' + newline
        if kind == 'fb':
            s+= f'''% of views from Facebook: {u.percentage(item['Fb refs'], total)}''' + newline
        elif kind == 'tw':
            s+= f'''% of views from Twitter: {u.percentage(item['Tw refs'], total)}''' + newline
        elif kind == 'li':
            s+= f'''% of views from LinkedIn: {u.percentage(item['Li refs'], total)}''' + newline
        else:
            s += f'''TRAFFIC %: social {u.percentage(item['Social refs'], tvu)}, search {u.percentage(item['Search refs'], tvu)}, other {u.percentage(item['Other refs'], tvu)}, direct {u.percentage(item['Direct refs'], tvu)}, internal {u.percentage(item['Internal refs'], tvu)}''' + newline
            s += f'''SOCIAL BREAKDOWN %: FB {u.percentage(item['Fb refs'], ts)}, Twitter {u.percentage(item['Tw refs'], ts)} | Interactions: {u.humanize(item["Social interactions"])}''' + newline
            s += f'''DEVICES %: mobile {u.percentage(item['Mobile views'], tvu)}, desktop {u.percentage(item['Desktop views'], tvu)}, tablet {u.percentage(item['Tablet views'], tvu)}''' + newline
        s += f'---------------------------' + newline
    s += "======================\n"
    return s


df = pd.read_csv(file_name,
                 usecols=cols_to_keep,
                 keep_default_na=False,
                 na_values='0')

df.columns = df.columns.str.replace('\xa0', ' ')

cols_to_fix = ["Search refs", "Internal refs", "Other refs", "Social refs", "Fb refs", "Tw refs", "Li refs", "Pi refs", "Social interactions", "Fb interactions", "Tw interactions"]

df[cols_to_fix] = df[cols_to_fix].apply(pd.to_numeric)

# TOP FB ARTICLES
articles_top_FB = df.sort_values(by=['Fb refs'], ascending=False).head(3).to_dict(orient='records')
FB_views = df['Fb refs'].sum()
# print(articles_top_FB)
report = 'Top articles by PV from Facebook\n================\n'
report += article_stats(articles_top_FB, 'fb', FB_views)

# TOP Twitter ARTICLES
articles_top_TW = df.sort_values(by=['Tw refs'], ascending=False).head(3).to_dict(orient='records')
TW_views = df['Tw refs'].sum()
# print(articles_top_FB)
report += 'Top articles by PV from Twitter\n================\n'
report += article_stats(articles_top_TW, 'tw', TW_views)

# TOP Twitter ARTICLES
articles_top_LI = df.sort_values(by=['Li refs'], ascending=False).head(3).to_dict(orient='records')
LI_views = df['Li refs'].sum()
# print(articles_top_FB)
report += 'Top articles by PV from LinkedIn\n================\n'
report += article_stats(articles_top_LI, 'li', LI_views)

print(report)
# print(df.dtypes)
