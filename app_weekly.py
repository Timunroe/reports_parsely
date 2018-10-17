import pyperclip
import utils_weekly

# DYNAMIC VALUES
weekly_file_path = 'spec/weekly/' + 'Site-Stats-Over-Time-Oct-07-2018-Oct-13-2018-thespec-com.csv'
ma_file_path = 'spec/3_month_avg/' + 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-thespec-com.csv'
ma_days = 12
posts_file_path = 'spec/weekly/' + 'Top-20-posts-by-total-engaged-minutes-Oct-07-2018-Oct-13-2018-thespec-com.csv'

# search daily folder, find latest 'stats over time', then look for matching 'top 10 posts'.
# bob = utils_weekly.newest('spec/daily/')
# print(bob)

# STATIC VALUES
dbl_line = '===========================================================\n'
sngl_line = '-----------------------------------------------------------\n'
nl = '\n'

# MAIN
weekly_values = utils_weekly.return_csv(weekly_file_path)
ma_values = utils_weekly.return_csv(ma_file_path)
posts_values = utils_weekly.return_csv(posts_file_path)
data = utils_weekly.site_stats(weekly_values, ma_values, ma_days)

# posts = utils_weekly.post_stats()
s = ''
s += f'Weekly report: thespec.com for {weekly_values["Date"]}' + nl + nl
s += f"Based on *post* views"
s += f", about {utils_weekly.percentage(data['postv']['new'], data['pagev']['new'])}% of total page views" + nl
s += dbl_line
s += f'''SITE         Totals | Diff. | KPIs
DETAILS:            | vs MA |
'''
s += sngl_line
s += f"{'Post views'.ljust(10)}  {utils_weekly.humanize_number(data['postv']['new'],0).rjust(6)} "
s += f"{data['postv']['delta'].rjust(8)}   {data['postv']['kpi_new']} views/vis." + nl
s += f"{'Visitors'.ljust(10)}  {utils_weekly.humanize_number(data['visitors']['new'],0).rjust(6)}    --------------------------------------" + nl
s += f"{'Minutes'.ljust(10)}  {utils_weekly.humanize_number(data['minutes']['new'],0).rjust(6)} "
s += f"{data['minutes']['delta'].rjust(8)}   {data['minutes']['kpi_new']} minutes/vis." + nl
s += dbl_line
s += f"TRAFFIC DETAILS:  % of views  |  VISITORS %:" + nl
s += f"----------------------------- |  New {data['visitor_type']['new']}, Returning {data['visitor_type']['returning']}" + nl
s += f"{'*Search & Other'.ljust(16)} {(utils_weekly.percentage(data['traffic']['s+o'], data['postv']['new'])).rjust(6)}"
s += f"       |  --------------------------" + nl
s += f"{'Internal'.ljust(16)} {(utils_weekly.percentage(data['traffic']['internal'], data['postv']['new'])).rjust(6)}"
s += f"       |  DEVICES %:" + nl
s += f"{'Direct'.ljust(16)} {(utils_weekly.percentage(data['traffic']['direct'], data['postv']['new'])).rjust(6)}"
s += f"       |  Mobile {data['devices']['mobile']}" + nl
s += f"{'Facebook'.ljust(16)} {(utils_weekly.percentage(data['traffic']['fb'], data['postv']['new'])).rjust(6)}"
s += f"       |  Desktop {data['devices']['desktop']}" + nl
s += f"{'Twitter'.ljust(16)} {(utils_weekly.percentage(data['traffic']['tco'], data['postv']['new'])).rjust(6)}"
s += f"       |  Tablet {data['devices']['tablet']}" + nl
s += sngl_line
s += f"Note: MA = 3-month moving average" + nl
s += f"Due to rounding, numbers may not add up to 100%\n" 
s += f"* Google search accounts for most 'Search' views.\n* Google News and Google APIs account for most 'Other' views."
s += nl + dbl_line
s += nl + dbl_line
s += "TOP POSTS: by Total Engaged Minutes" + nl + sngl_line

for rank, item in enumerate(posts_values[:7], start=1):
    s += f'''{rank}. {item['Title'].title().replace('’T','’t').replace('’S', '’s').replace('’M','’m').replace('’R','’r')}\nBy {item['Authors'].title()} in {item['Section']}
\n\
VISITORS: {str(round(float(item['Sort (Engaged minutes)'])/float(item['Visitors']),2))} min/visitor, visitors: {utils_weekly.humanize_number(item['Visitors'],1)}, returning: {(utils_weekly.percentage(item['Returning vis.'], item['Visitors']))}%
TRAFFIC %: social {(utils_weekly.percentage(item['Social refs'], item['Views']))}, search & other {(utils_weekly.percentage((float(item['Search refs']) +float(item['Other refs'])), item['Views']))}, \
internal {(utils_weekly.percentage(item['Internal refs'], item['Views']))}
DEVICES %: mobile {(utils_weekly.percentage(item['Mobile views'], item['Views']))}, desktop {(utils_weekly.percentage(item['Desktop views'], item['Views']))}, tablet {(utils_weekly.percentage(item['Tablet views'], item['Views']))}\
'''
    s += nl + nl + sngl_line

# print(s)
# pprint.pprint(posts_values)
pyperclip.copy(s)

# save as text file. Note, this overwrites the file.
with open("weekly.txt", "w") as f:
    f.write(s)
