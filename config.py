weekly_start_stats = 'Nov-18'
# weekly_start_top = 'Feb-09'
weekly_end = 'Feb-23'
monthly_start_top = "Feb-01"
monthly_start_stats = "Nov-01"
monthly_end = "Feb-28"

# reference file, stats, will have target period plus 90 days' worth of MA.
# example, daily stats will have previous 91 days - compare last day versus the other 90
# monthly stats will have 4 months - previous month (first item in array), compared with other months in file
# target period is always a[0:1]
# MA is always a[1:]

# timeanddate.com
# Subtract 91 days from today, to get yesterday and 90 more days in Parsely report - group by day!
# subtract 14 weeks from last Saturday, to get last week and 13 more weesks
#  in Parsely report - group by week!

# CREATE PDF
# enscript -B -M A5 -p output.ps input.txt
# ps2pdf output.ps output.pdf

# how many top posts do we want to show in report?
slice_var = {
    "daily": slice(0, 8),
    "weekly": slice(0, 10),
    "monthly": slice(0, 15),
}

files = {
    "spectator": {
        "daily": {
            'stats': 'Spec-site-stats-91-days.csv',
            "posts": 'Spec-top-posts-byMinutes-yesterday.csv',
        },
        "weekly": {
            'stats': f'Spec-Site-Stats-Over-Time-14-weeks.csv',
            "posts": 'Spec-top-posts-byMinutes-lastWeek.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2019-thespec-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2019-{monthly_end}-2019-thespec-com-post.csv',
        }
    },
    "record": {
        "daily": {
            'stats': f'Rec-site-stats-91-days.csv',
            "posts": f'Rec-top-posts-byMinutes-yesterday.csv',
            "ma": 'Site-Stats-Over-Time-Aug-01-2018-Oct-31-2018-therecord-com.csv'
        },
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2019-therecord-com-Website-post.csv',
            "posts": 'Rec-Top20-posts-by-minutes-last-week-therecord-com-post.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2019-therecord-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2019-{monthly_end}-2019-therecord-com-post.csv',
        }
    },
    "niagara": {
        "weekly": {
            'stats': f'Site-Group-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2019-None-Niagara-Region-Dailies-Website-post.csv',
            "posts": 'Niagara-top20-by-minutes-last-week-None-Niagara-Region-Dailies-post.csv',
        },
        "monthly": {
            'stats': f'Site-Group-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2019-None-Niagara-Region-Dailies-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2019-{monthly_end}-2019-None-Niagara-Region-Dailies-post.csv',
        }
    },
    "examiner": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2019-thepeterboroughexaminer-com-Website-post.csv',
            "posts": 'Examiner-top20-posts-by-minutes-last-week-thepeterboroughexaminer-com-post.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2019-thepeterboroughexaminer-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2019-{monthly_end}-2019-thepeterboroughexaminer-com-post.csv',
        }
    },
    "star": {
        "weekly": {
            'stats': f'Site-Stats-Over-Time-{weekly_start_stats}-2018-{weekly_end}-2019-thestar-com-Website-post.csv',
            "posts": 'Star-top20-posts-by-minutes-last-week-thestar-com-Website-post.csv',
        },
        "monthly": {
            'stats': f'Site-Stats-Over-Time-{monthly_start_stats}-2018-{monthly_end}-2019-thestar-com-Website-post.csv',
            "posts": f'Top-20-posts-by-total-engaged-minutes-{monthly_start_top}-2019-{monthly_end}-2019-thestar-com-post.csv',
        }
    },
}
