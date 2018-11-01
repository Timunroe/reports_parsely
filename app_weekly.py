import pyperclip
import sys
import utils

if len(sys.argv) > 1:
    if (sys.argv)[1] == 'record':
        site = 'record'
    elif (sys.argv)[1] == 'standard':
        site = 'standard'
    elif (sys.argv)[1] == 'examiner':
        site = 'examiner'
    elif (sys.argv)[1] == 'star':
        site = 'star'
else:
    site = 'spectator'
print("Site is: ", site)

# DYNAMIC VALUES
files = {
    "spectator": {
        "weekly": 'Site-Stats-Over-Time-Oct-21-2018-Oct-27-2018-thespec-com.csv',
        "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-21-2018-Oct-27-2018-thespec-com-post.csv',
        "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thespec-com.csv'
    },
    "record": {
        "weekly": 'Site-Stats-Over-Time-Oct-21-2018-Oct-27-2018-therecord-com.csv',
        "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-21-2018-Oct-27-2018-therecord-com-post.csv',
        "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-therecord-com.csv'
    },
    "standard": {
        "weekly": 'Site-Stats-Over-Time-Oct-21-2018-Oct-27-2018-stcatharinesstandard-ca.csv',
        "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-21-2018-Oct-27-2018-stcatharinesstandard-ca-post.csv',
        "ma": 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-stcatharinesstandard-ca.csv'
    },
    "examiner": {
        "weekly": 'Site-Stats-Over-Time-Oct-21-2018-Oct-27-2018-thepeterboroughexaminer-com.csv',
        "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-21-2018-Oct-27-2018-thepeterboroughexaminer-com-post.csv',
        "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv'
    },
    "star": {
        "weekly": 'Site-Stats-Over-Time-Oct-21-2018-Oct-27-2018-thestar-com.csv',
        "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-21-2018-Oct-27-2018-thestar-com-post.csv',
        "ma": 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-thestar-com.csv'
    },
}

weekly_file_path = 'reports/weekly/' + files[site]['weekly']
posts_file_path = 'reports/weekly/' + files[site]['posts']
ma_file_path = 'reports/3_month_avg/' + files[site]['ma']
ma_units = 92/7

# search daily folder, find latest 'stats over time', then look for matching 'top 10 posts'.
# bob = utils.newest('spec/daily/')
# print(bob)

# STATIC VALUES
dbl_line = '===========================================================\n'
sngl_line = '-----------------------------------------------------------\n'
nl = '\n'

# MAIN
weekly_values = utils.return_csv(weekly_file_path)
ma_values = utils.return_csv(ma_file_path)
posts_values = utils.return_csv(posts_file_path)
data = utils.site_stats(weekly_values, ma_values, ma_units)

# posts = utils.post_stats()
s = ''
s += f'Weekly web report: {site.title()} for week starting {weekly_values["Date"]}' + nl + nl
s += dbl_line
s += "TOP POSTS: by Total Engaged Minutes" + nl + sngl_line

for rank, item in enumerate(posts_values[:7], start=1):
    s += f'''{rank}. {item['Title'].title().replace('’T','’t').replace('’S', '’s').replace("'S","'s").replace('’M','’m').replace('’R','’r')}\nBy {item['Authors'].title()} in {item['Section']}''' + nl + nl
    s += f"VISITORS: {str(round(float(item['Sort (Engaged minutes)'])/float(item['Visitors']),2))} min/visitor, "
    s += f"visitors: {utils.humanize_number(item['Visitors'],1)}, returning: {(utils.percentage(item['Returning vis.'], item['Visitors']))}%" + nl
    s += f"TRAFFIC %: social {(utils.percentage(item['Social refs'], item['Views']))}, "
    s += f"search&other {utils.percentage(utils.sum_safe([ item['Search refs'], item['Other refs'] ]), item['Views'])}, "
    s += f"internal {(utils.percentage(item['Internal refs'], item['Views']))}, direct {(utils.percentage(item['Direct refs'], item['Views']))}" + nl
    s += f"DEVICES %: mobile {(utils.percentage(item['Mobile views'], item['Views']))}, desktop {(utils.percentage(item['Desktop views'], item['Views']))}, "
    s += f"tablet {(utils.percentage(item['Tablet views'], item['Views']))}"
    s += nl + nl + sngl_line

s += nl
s += dbl_line
s += f'''SITE         Totals | Diff. | KPIs
DETAILS:            | vs MA |
'''
s += sngl_line
s += f"{'Post views'.ljust(10)}  {utils.humanize_number(data['postv']['new'],0).rjust(6)} "
s += f"{data['postv']['delta'].rjust(8)}   {data['postv']['kpi_new']} views/vis." + nl
s += f"{'Visitors'.ljust(10)}  {utils.humanize_number(data['visitors']['new'],0).rjust(6)}    --------------------------------------" + nl
s += f"{'Minutes'.ljust(10)}  {utils.humanize_number(data['minutes']['new'],0).rjust(6)} "
s += f"{data['minutes']['delta'].rjust(8)}   {data['minutes']['kpi_new']} minutes/vis." + nl
s += dbl_line
s += f"TRAFFIC DETAILS:  % of views  |  VISITORS %:" + nl
s += f"----------------------------- |  New {data['visitor_type']['new']}, Returning {data['visitor_type']['returning']}" + nl
s += f"{'Search + Others'.ljust(16)} {(utils.percentage(data['traffic']['s+o'], data['postv']['new'])).rjust(6)}"
s += f"       |  --------------------------" + nl
s += f"{'Internal'.ljust(16)} {(utils.percentage(data['traffic']['internal'], data['postv']['new'])).rjust(6)}"
s += f"       |  DEVICES %:" + nl
s += f"{'Direct'.ljust(16)} {(utils.percentage(data['traffic']['direct'], data['postv']['new'])).rjust(6)}"
s += f"       |  Mobile {data['devices']['mobile']}" + nl
s += f"{'Facebook'.ljust(16)} {(utils.percentage(data['traffic']['fb'], data['postv']['new'])).rjust(6)}"
s += f"       |  Desktop {data['devices']['desktop']}" + nl
s += f"{'Twitter'.ljust(16)} {(utils.percentage(data['traffic']['tco'], data['postv']['new'])).rjust(6)}"
s += f"       |  Tablet {data['devices']['tablet']}" + nl
s += sngl_line
s += f"Notes: MA = 3-month moving average" + nl
s += f"Due to rounding, numbers may not add up to 100%" + nl
s += f"Google search accounts for nearly all 'Search' views.\nGoogle News and Google APIs account for most 'Other' views." + nl
s += f"Based on *post* views"
s += f", about {utils.percentage(data['postv']['new'], data['pagev']['new'])}% of day's page views" + nl + dbl_line

# print(s)
# pprint.pprint(posts_values)
pyperclip.copy(s)

# save as text file. Note, this overwrites the file.
with open(f"weekly_{site}.txt", "w") as f:
    f.write(s)
