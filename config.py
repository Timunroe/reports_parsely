daily_date = '26'
daily_start_stats = "Sep-28"
daily_month = 'Dec'
weekly_start_stats = 'Sep-30'
weekly_start_top = 'Dec-23'
weekly_end = 'Dec-29'
monthly_start_top = "Dec-01"
monthly_start_stats = "Sep-01"
monthly_end = "Dec-31"

# reference file, stats, will have target period plus 90 days' worth of MA.
# example, daily stats will have previous 91 days - compare last day versus the other 90
# monthly stats will have 4 months - previous month (first item in array), compared with other months in file
# target period is always a[0:1]
# MA is always a[1:]

slice_var = {
    "daily": slice(0, 8),
    "weekly": slice(0, 10),
    "monthly": slice(0, 15),
}

files = {
    "spectator": {
        "daily": {
            'stats': f'Site-Stats-Over-Time-{daily_start_stats}-2018-{daily_month}-{daily_date}-2018-thespec-com-Website-post.csv',
            "posts": f'Top-10-posts-by-total-engaged-minutes-{daily_month}-{daily_date}-2018-thespec-com-post.csv',
        },
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-thespec-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-thespec-com-post.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2018-thespec-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2018-{monthly_end}-2018-thespec-com-post.csv',
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
            'stats': f'Site-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2018-therecord-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2018-{monthly_end}-2018-therecord-com-post.csv',
        }
    },
    "niagara": {
        "weekly": {
            'stats': f'Site-Group-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-None-Niagara-Region-Dailies-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-None-Niagara-Region-Dailies-post.csv',
        },
        "monthly": {
            'stats': f'Site-Group-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2018-None-Niagara-Region-Dailies-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2018-{monthly_end}-2018-None-Niagara-Region-Dailies-post.csv',
        }
    },
    "examiner": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-thepeterboroughexaminer-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-thepeterboroughexaminer-com-post.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2018-thepeterboroughexaminer-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2018-{monthly_end}-2018-thepeterboroughexaminer-com-post.csv',
        }
    },
    "star": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2018-thestar-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{weekly_start_top}-2018-{weekly_end}-2018-thestar-com-post.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2018-thestar-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2018-{monthly_end}-2018-thestar-com-post.csv',
        }
    },
}
