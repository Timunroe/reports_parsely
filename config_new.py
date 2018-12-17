daily_date = '06'
daily_month = 'Dec'
weekly_start_stats = 'Sep-16'
weekly_start_top = 'Dec-09'
weekly_end = 'Dec-15'
monthly_start = "Nov-01"
monthly_end = "Nov-30"


# new weekly file: has target week AND refrerence weeks all in one file
# weekly : 13 weeks in total
# daily: 90 days in total
# monthly: 3 months in total
# weekly/f'Site-Stats-Over-Time-{weekly_start}-2018-{weekly_end}-2018-thespec-com-Website-post.csv'

units = {
    'daily': 92,
    'weekly': 92 / 7,
    'monthly': 3,
}

slice_var = {
    'daily': slice(0, 8),
    'weekly': slice(0, 10),
    'monthly': slice(0, 15)
}

files = {
    "spectator": {
        "daily": {
            'stats': f'Site-Stats-Over-Time-{daily_month}-{daily_date}-2018-thespec-com.csv',
            "posts": f'Top-10-posts-by-total-engaged-minutes-{daily_month}-{daily_date}-2018-thespec-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Sep-01-2018-Nov-30-2018-thespec-com.csv'
        },
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-thespec-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-thespec-com-post.csv',       
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start}-2018-{monthly_end}-2018-thespec-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start}-2018-{monthly_end}-2018-thespec-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Sep-01-2018-Nov-30-2018-thespec-com.csv'
        }
    },
    "record": {
        "daily": {
            'stats': f'Site-Stats-Over-Time-{daily_month}-{daily_date}-2018-therecord-com.csv',
            "posts": f'Top-10-posts-by-total-engaged-minutes-{daily_month}-{daily_date}-2018-therecord-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-therecord-com.csv'
        },
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-therecord-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-therecord-com-post.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start}-2018-{monthly_end}-2018-therecord-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start}-2018-{monthly_end}-2018-therecord-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-therecord-com.csv'
        }
    },
    "standard": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-stcatharinesstandard-ca.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-stcatharinesstandard-ca-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-stcatharinesstandard-ca.csv'
        },
        "monthly": {
            'stats': 'Site-Stats-Over-Time-Oct-01-2018-Oct-31-2018-stcatharinesstandard-ca.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-01-2018-Oct-31-2018-stcatharinesstandard-ca-post.csv',
            "ma": 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-stcatharinesstandard-ca.csv'
        }
    },
    "niagara": {
        "weekly": {
            'stats': f'Site-Group-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-None-Niagara-Region-Dailies-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-None-Niagara-Region-Dailies-post.csv',
        },
        "monthly": {
            'stats': f'Site-Group-Stats-Over-Time-{monthly_start}-2018-{monthly_end}-2018-None-Niagara-Region-Dailies.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start}-2018-{monthly_end}-2018-None-Niagara-Region-Dailies-post.csv',
            "ma": 'Site-Group-Stats-Over-Time-Aug-01-2018-Oct-31-2018-None-Niagara-Region-Dailies.csv'
        }
    },
    "examiner": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-thepeterboroughexaminer-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-thepeterboroughexaminer-com-post.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start}-2018-{monthly_end}-2018-thepeterboroughexaminer-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start}-2018-{monthly_end}-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv'
        }
    },
    "review": {
        "weekly": {
            'stats': 'Site-Stats-Over-Time-Oct-28-2018-Nov-03-2018-thepeterboroughexaminer-com.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-28-2018-Nov-03-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv'
        },
        "monthly": {
            'stats': 'Site-Stats-Over-Time-Oct-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-01-2018-Oct-31-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv'
        }
    },
    "tribune": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-thepeterboroughexaminer-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv'
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start}-2018-{monthly_end}-2018-thepeterboroughexaminer-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start}-2018-{monthly_end}-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv'
        }
    },
    "star": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-thestar-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-thestar-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thestar-com.csv'
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start}-2018-{monthly_end}-2018-thestar-com-Website.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start}-2018-{monthly_end}-2018-thestar-com-Website-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thestar-com-Website.csv'
        }
    },
}
