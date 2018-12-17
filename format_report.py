import utils_new

# STATIC VALUES
dbl_line = '\n===========================================================\n'
sngl_line = '\n-----------------------------------------------------------\n'
nl = '\n'


def format_posts(data):
    # data is a list of dicts
    s = ''
    s += dbl_line + "TOP POSTS: by Total Engaged Minutes" + sngl_line
    for rank, item in enumerate(data, start=1):
        headline = item['Title'].title().replace('’T', '’t').replace('’S', '’s').replace("'S", "'s").replace('’M', '’m').replace('’R', '’r')
        author = item['Authors'].title()
        section = item['Section']
        mv = str(round(float(item['Sort (Engaged minutes)']) / float(item['Visitors']), 2))
        v = utils_new.humanize_number(item['Visitors'], 1)
        r = (utils_new.percentage(item['Returning vis.'], item['Visitors']))
        so = (utils_new.percentage(item['Social refs'], item['Views']))
        se = (utils_new.percentage(item['Search refs'], item['Views']))
        o = (utils_new.percentage(item['Other refs'], item['Views']))
        i = (utils_new.percentage(item['Internal refs'], item['Views']))
        di = (utils_new.percentage(item['Direct refs'], item['Views']))
        mo = (utils_new.percentage(item['Mobile views'], item['Views']))
        de = (utils_new.percentage(item['Desktop views'], item['Views']))
        ta = (utils_new.percentage(item['Tablet views'], item['Views']))
        fb = (utils_new.percentage(item['Fb refs'], item['Social refs']))
        tw = (utils_new.percentage(item['Tw refs'], item['Social refs']))
        inte = utils_new.humanize_number(item['Social interactions'], 1)

        s += f'''{rank}. {headline}
By {author} in {section}
VISITORS: {mv} min/visitor, visitors: {v}, returning: {r}%
TRAFFIC %: social {so}, search {se}, other {o}, direct {di}, internal {i}
SOCIAL BREAKDOWN %: FB {fb}, Twitter {tw} | Interactions: {inte}
DEVICES %: mobile {mo}, desktop {de}, tablet {ta}

-----------------------------------------------------------\n'''
    return s


def format_site(data):
    # data is a dict
    text = ''
    a = (utils_new.humanize_number(data['postv']['new'], 0)).rjust(4)
    b = (data['postv']['delta']).rjust(5)
    c = (data['postv']['kpi_new']).ljust(4)
    d = (utils_new.humanize_number(data['visitors']['new'], 0)).rjust(4)
    e = (data['visitors']['delta']).rjust(5)
    f = (utils_new.humanize_number(data['minutes']['new'], 0)).rjust(4)
    g = (data['minutes']['delta']).rjust(5)
    h = (data['minutes']['kpi_new']).ljust(4)
    i = utils_new.percentage(data['postv']['new'], data['pagev']['new'])
    j = data['traffic']['fb%'].rjust(2)
    k = data['traffic']['fb_ma%'].rjust(2)
    l = data['visitor_type']['new'].rjust(2)
    m = data['visitor_type']['new_ma%'].rjust(2)
    n = data['traffic']['tco%'].rjust(2)
    o = data['traffic']['tco_ma%'].rjust(2)
    p = data['visitor_type']['returning'].rjust(2)
    q = data['visitor_type']['returning_ma%'].rjust(2)
    r = data['traffic']['search%'].rjust(2)
    s = data['traffic']['search_ma%'].rjust(2)
    t = data['traffic']['other%'].rjust(2)
    u = data['traffic']['other_ma%'].rjust(2)
    v = data['traffic']['direct%'].rjust(2)
    w = data['traffic']['direct_ma%'].rjust(2)
    x = data['traffic']['internal%'].rjust(2)
    y = data['traffic']['internal_ma%'].rjust(2)
    z = data['devices']['mobile%'].rjust(2)
    aa = data['devices']['mobile_ma%'].rjust(2)
    bb = data['devices']['desktop%'].rjust(2)
    cc = data['devices']['desktop_ma%'].rjust(2)
    dd = data['devices']['tablet%'].rjust(2)
    ee = data['devices']['tablet_ma%'].rjust(2)
    if len(data['pagev']['new']) > 6:
        ff = (utils_new.humanize_number(data['pagev']['new'], 1)).rjust(4)
    else:
        ff = (utils_new.humanize_number(data['pagev']['new'], 0)).rjust(4)
    gg = (data['pagev']['delta']).rjust(5)
    hh = (data['pagev']['kpi_new']).ljust(4)
    ii = (utils_new.humanize_number(data['visitors']['new_pages'], 0)).rjust(4)
    jj = (data['visitors']['total_delta']).rjust(5)
    kk = (utils_new.humanize_number(data['minutes']['new_pages'], 0)).rjust(4)
    ll = (data['minutes']['total_delta']).rjust(5)
    mm = (data['minutes']['kpi_pages']).ljust(4)
    text += f'''
===================================================
SITE DETAILS    Last | vs Last  | KPIs
[POST PAGES]    Week | 13 Weeks |
---------------------------------------------------
Post views      {a}    {b}     {c} views/vis.
Post visitors   {d}    {e}     -----------------
Post minutes    {f}    {g}     {h} minutes/vis.
---------------------------------------------------
* Post views were {i}% of period's total page views
---------------------------------------------------
Page views      {ff}    {gg}     {hh} views/vis.
Page visitors   {ii}    {jj}     -----------------
Page minutes    {kk}    {ll}     {mm} minutes/vis.
===================================================
POST       Last  Last 13 |  VISITOR   Last  Last 13
TRAFFIC:   Week   Weeks  |  PROFILE:  Week   Weeks
---------------------------------------------------
Facebook    {j}     {k}    |  New        {l}     {m}
Twitter     {n}     {o}    |  Returning  {p}     {q}
Search      {r}     {s}    |  -----------------------
Other       {t}     {u}    |  DEVICES:
Direct      {v}     {w}    |  Mobile     {z}     {aa}
Internal    {x}     {y}    |  Desktop    {bb}     {cc}
                         |  Tablet     {dd}     {ee}
---------------------------------------------------
Due to rounding, numbers may not add up to 100%
Google search accounts for nearly all 'Search' views.
Google News, APIs account for most 'Other' views.
===================================================
'''
    return text


def format_data(data):
    s = ''
    s += f'''{data["report"].title()} web report: {data["site"].title()} for {data["report"].replace("daily", "").replace("ly", "")} {data["site_stats"]["date"]}''' + nl + nl
    s += dbl_line
    # s += format_posts(data['posts_stats'])
    s += format_site(data['site_stats'])
    return s
