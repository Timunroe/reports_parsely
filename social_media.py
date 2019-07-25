# default
import random
# 3rd party
import pandas as pd
from requests_html import HTMLSession
# from requests_html import HTML
from bullet import Check
import requests
# from bs4 import BeautifulSoup
# mine
from utils import utils_io

# overview of social networks (Facebook, Twitter, LinkedIn, Instagram, Pinterest)
# how much traffic do we see, performance of our posts
# FACEBOOK
# Followers: xxx,
# Posts: xxx,
# Impressions: xxx, reach: xxx

# TWITTER
# Followers:
# Posts: xxx,
# Impressions: xxxx,

# ---[ FUNCTIONS ]-------------


def process_csv(file_name, folders, cols_to_keep=None):
    # file_name: str
    # folders: list of subdirectories
    data = utils_io.get_file(file_name, folders)
    fixed_csv = data.replace('.0', '').replace('\xa0', ' ')\
        .replace(',,,,', ',0,0,0,').replace(',,,', ',0,0,')\
        .replace(',,', ',0,').replace(',\n', ',0\n')
    # TEST POINT
    # print(fixed_csv)
    if cols_to_keep:
        df = pd.read_csv(pd.compat.StringIO(fixed_csv), usecols=cols_to_keep)
    # df = pd.read_csv(file_name, usecols=cols_to_keep, keep_default_na=False, na_values='0')
    else:
        df = pd.read_csv(pd.compat.StringIO(fixed_csv))
    return df


def get_follower_count(site, url):
    r = session.get(url)
    if site == 'facebook':
        temp = r.html.find('div._4bl9 > div')
        return temp[2].text.replace(' people follow this', '')
    if site == 'twitter':
        temp = r.html.find('li.ProfileNav-item--followers > a > span.ProfileNav-value', first=True)
        return temp.attrs['data-count']
    if site == 'instagram':
        temp = r.html.find('head', first=True)
        # temp = r.html.find('head', first=True)
        temp2 = temp.find('meta[property="og:description"]', first=True)
        temp3 = temp2.attrs['content']
        return temp3[0:5]
    if site == 'linkedin':
        # temp = r.html.render(sleep=8)
        r = requests.get('https://ca.linkedin.com/company/waterloo-region-record')
        print(r.text)
        # temp = r.html.find('head', first=True)
        return r


# ---[ MAIN ]-------------

session = HTMLSession()

reports = ["daily", "weekly", "monthly"]
sites = ["Spectator", "Record", "Standard", "Review", "Tribune", "Examiner"]

site_cols_keep = [
    'Post Message',
    'Type',
    'Posted',
    'Lifetime Post organic reach',
    'Lifetime Post viral reach',
    'Lifetime Post Organic Impressions',
    'Lifetime Post Viral Impressions',
    'Lifetime Engaged Users',
    'Lifetime People who have liked your Page and engaged with your post',
    'Lifetime Post Audience Targeting Unique Consumptions by Type - link clicks',
]

cli = Check(
    prompt="\nChoose report: ",
    choices="Follower counts",
    # choices=(reports + sites),
    indent=0,
    align=5,
    margin=2,
    shift=0,
    check="√",
    pad_right=5
)
feedback = cli.launch()  # Launch a prompt
# error control
# only 2 selectsions, one must be in ['daily', 'weekly', 'monthly']

# Get social network followers
networks = {
    'spectator': [
        ('facebook', 'https://www.facebook.com/hamiltonspectator/'),
        ('twitter', 'https://twitter.com/thespec'),
        ('instagram', 'https://www.instagram.com/hamiltonspectator/'),
        ('linkedin', 'https://ca.linkedin.com/company/the-hamilton-spectator')
    ],
    'record': [
        ('facebook', 'https://www.facebook.com/hamiltonspectator/'),
        ('twitter', 'https://twitter.com/thespec'),
        ('linkedin', 'https://ca.linkedin.com/company/waterloo-region-record')
    ],
}

if feedback[0] in reports:
    freq = feedback[0]
else:
    print("No report frequency chosen.")
if feedback[1] in sites:
    site = feedback[1]
else:
    print("No site chosen.")

# fb_count = get_count('facebook', 'https://www.facebook.com/hamiltonspectator/')
# tw_count = get_count('twitter', 'https://twitter.com/thespec')
# in_count = get_count('instagram', 'https://www.instagram.com/hamiltonspectator/')

df = process_csv('spectator_facebook.csv', ['data_in', 'weekly'], site_cols_keep)
df['Posted'] = pd.to_datetime(df['Posted'])
df.columns = ['Post Message', 'Type', 'Posted', 'Viral Reach', 'Viral Impressions', 'Organic Reach', 'Organic Impressions', 'Engaged Users', 'Engaged Fans', 'Link Clicks']
df['% own fans'] = round((df['Engaged Fans'] / df['Engaged Users']) * 100, 0)
df['Reach'] = df['Organic Reach'] + df['Viral Reach']
df['Organic Reach %'] = round((df['Organic Reach'] / df['Reach']) * 100, 0)
df['Viral Reach %'] = round((df['Viral Reach'] / df['Reach']) * 100, 0)

df['Impressions'] = df['Organic Impressions'] + df['Viral Impressions']
df['Organic Impressions %'] = round((df['Organic Impressions'] / df['Impressions']) * 100, 0)
df['Viral Impressions %'] = round((df['Viral Impressions'] / df['Impressions']) * 100, 0)

df['CTR Impressions'] = round((df['Link Clicks'] / df['Impressions']) * 100, 1)
df['CTR Reach'] = round((df['Link Clicks'] / df['Reach']) * 100, 1)

# print(df.columns)

posts = len(df.index)
impressions = df['Impressions'].sum()
reach = df['Reach'].sum()
impressions_ctr = round((df['Link Clicks'].sum() / impressions) * 100, 1)
reach_ctr = round((df['Link Clicks'].sum() / reach) * 100, 1)
own_fans = round((df['Engaged Fans'].sum() / df['Engaged Users'].sum()) * 100, 0)
impressions_per_post = int(round(impressions / posts, 0))
reach_per_post = int(round(reach / posts, 0))

s = f'{site.title()}\n'
s += f'''Facebook posts: {str(posts)}\n'''
s += f'''  Impressions: {str(impressions)}\n'''
s += f'''  Reach: {str(reach)}\n'''
s += f'''  Impressions CTR: {str(impressions_ctr)}%\n'''
s += f'''  Reach CTR: {str(reach_ctr)}%\n'''
s += f'''  Own Fans: {str(own_fans)}%\n'''
s += f''' Impressions per post: {str(impressions_per_post)}\n'''
s += f''' Reach per post: {str(reach_per_post)}\n'''

print(s)

# print(f'''{fb_count} FB followers, {tw_count} Twitter followers, {in_count} Instagram followers.''')
