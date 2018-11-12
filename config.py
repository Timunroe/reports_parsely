daily_date = '10'
daily_month = 'Nov'
weekly_start = 'Nov-04'
weekly_end = 'Nov-10'

units = {
    'daily': 92,
    'weekly': 92/7,
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
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thespec-com.csv'
        },
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start}-2018-{weekly_end}-2018-thespec-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start}-2018-{weekly_end}-2018-thespec-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thespec-com.csv'
        },
        "monthly": {
            'stats': 'Site-Stats-Over-Time-Oct-01-2018-Oct-31-2018-thespec-com.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-01-2018-Oct-31-2018-thespec-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thespec-com.csv'
        }
    },
    "record": {
        "daily": {
            'stats': f'Site-Stats-Over-Time-{daily_month}-{daily_date}-2018-therecord-com.csv',
            "posts": f'Top-10-posts-by-total-engaged-minutes-{daily_month}-{daily_date}-2018-therecord-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-therecord-com.csv'
        },
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start}-2018-{weekly_end}-2018-therecord-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start}-2018-{weekly_end}-2018-therecord-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-therecord-com.csv'
        },
        "monthly": {
            'stats': 'Site-Stats-Over-Time-Oct-01-2018-Oct-31-2018-therecord-com.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-01-2018-Oct-31-2018-therecord-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thespec-com.csv'
        }
    },
    "standard": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start}-2018-{weekly_end}-2018-stcatharinesstandard-ca.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start}-2018-{weekly_end}-2018-stcatharinesstandard-ca-post.csv',
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
            'stats': f'Site-Group-Stats-Over-Time-{weekly_start}-2018-{weekly_end}-2018-None-Niagara-Region-Dailies.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start}-2018-{weekly_end}-2018-None-Niagara-Region-Dailies-post.csv',
            "ma": 'Site-Group-Stats-Over-Time-Aug-01-2018-Oct-31-2018-None-Niagara-Region-Dailies.csv'
        },
        "monthly": {
            'stats': 'Site-Stats-Over-Time-Oct-01-2018-Oct-31-2018-stcatharinesstandard-ca.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-01-2018-Oct-31-2018-stcatharinesstandard-ca-post.csv',
            "ma": 'Site-Group-Stats-Over-Time-Aug-01-2018-Oct-31-2018-None-Niagara-Region-Dailies.csv'
        }
    },
    "examiner": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start}-2018-{weekly_end}-2018-thepeterboroughexaminer-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start}-2018-{weekly_end}-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv'
        },
        "monthly": {
            'stats': 'Site-Stats-Over-Time-Oct-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-01-2018-Oct-31-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-thepeterboroughexaminer-com.csv'
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
            "ma": 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-thepeterboroughexaminer-com.csv'
        }
    },
    "tribune": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start}-2018-{weekly_end}-2018-thepeterboroughexaminer-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start}-2018-{weekly_end}-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv'
        },
        "monthly": {
            'stats': 'Site-Stats-Over-Time-Oct-01-2018-Oct-31-2018-thepeterboroughexaminer-com.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-01-2018-Oct-31-2018-thepeterboroughexaminer-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-thepeterboroughexaminer-com.csv'
        }
    },
    "star": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start}-2018-{weekly_end}-2018-thestar-com.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start}-2018-{weekly_end}-2018-thestar-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-thestar-com.csv'
        },
        "monthly": {
            'stats': 'Site-Stats-Over-Time-Oct-01-2018-Oct-31-2018-thestar-com.csv',
            "posts": 'Top-20-posts-by-total-engaged-minutes-Oct-21-2018-Oct-27-2018-thestar-com-post.csv',
            "ma": 'Site-Stats-Over-Time-Jul-01-2018-Sep-30-2018-thestar-com.csv'
        }
    },
}
