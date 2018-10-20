def site_stats(new, ma, days):
    result = {
        "pagev": {
            "new": new['Views (all pages)'],
            "avg": sum_csv_values(ma, 'Views (all pages)'),
            "delta": ''
        },
        "postv": {
            "new": new['Views (posts)'],
            "avg": sum_csv_values(ma, 'Views (posts)'),
            "delta": '',
            "kpi_new": '',
        },
        "visitors": {
            "new": new['Visitors (posts)'],
            "avg": sum_csv_values(ma, 'Visitors (posts)'),
            "delta": '',
        },
        "minutes": {
            "new": new['Engaged Minutes (posts)'],
            "avg": sum_csv_values(ma, 'Engaged Minutes (posts)'),
            "delta": '',
            "kpi_new": '',
        },
        "visitor_type": {
            "new": str(round((float(new['New vis.']) / float(new['Visitors (posts)']) * 100), 0)).replace('.0', ''),
            "returning": str(round((float(new['Returning vis.']) / float(new['Visitors (posts)'])*100), 0)).replace('.0', '')
        },
        "devices": {
            "mobile": new['Mobile views'],
            "desktop": new['Desktop views'],
            "tablet": new['Tablet views']
        },
        "traffic": {
            "s+o": str(float(new['Search refs']) + float(new['Other refs'])),
            "internal": new['Internal refs'],
            "direct": new['Direct refs'],
            "fb": new['Fb refs'],
            "tco": new['Tw refs']
        }
    }

    result['pagev']['delta'] = vs_ma(result['pagev']['new'], result['pagev']['avg'], days)
    result['postv']['delta'] = vs_ma(result['postv']['new'], result['postv']['avg'], days)
    result['visitors']['delta'] = vs_ma(result['visitors']['new'], result['visitors']['avg'], days)
    result['minutes']['delta'] = vs_ma(result['minutes']['new'], result['minutes']['avg'], days)
    result['devices']['mobile'] = percentage(result['devices']['mobile'], result['postv']['new'])
    result['devices']['desktop'] = percentage(result['devices']['desktop'], result['postv']['new'])
    result['devices']['tablet'] = percentage(result['devices']['tablet'], result['postv']['new'])
    result['postv']['kpi_new'] = str(round((float(result['postv']['new'])/float(result['visitors']['new'])), 2))
    result['minutes']['kpi_new'] = str(round((float(result['minutes']['new'])/float(result['visitors']['new'])), 2))
    return result
