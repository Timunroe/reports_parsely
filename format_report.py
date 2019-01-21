import utils as utils
import subprocess

# STATIC VALUES
dbl_line = '\n===========================================================\n'
sngl_line = '\n-----------------------------------------------------------\n'
nl = '\n'


def format_posts(data):
    # data is a list of dicts
    text = ''
    text += dbl_line + "TOP POSTS: by Total Engaged Minutes" + sngl_line
    for rank, item in enumerate(data, start=1):
        headline = item['Title'].title().replace('’T', '’t').replace('’S', '’s').replace("'S", "'s").replace('’M', '’m').replace('’R', '’r')
        author = item['Authors'].title()
        section = item['Section']
        mv = str(round(float(item['Sort (Engaged minutes)']) / float(item['Visitors']), 2))
        v = utils.humanize_number(item['Visitors'], 1)
        r = (utils.percentage(item['Returning vis.'], item['Visitors']))
        so = (utils.percentage(item['Social refs'], item['Views']))
        se = (utils.percentage(item['Search refs'], item['Views']))
        o = (utils.percentage(item['Other refs'], item['Views']))
        i = (utils.percentage(item['Internal refs'], item['Views']))
        di = (utils.percentage(item['Direct refs'], item['Views']))
        mo = (utils.percentage(item['Mobile views'], item['Views']))
        de = (utils.percentage(item['Desktop views'], item['Views']))
        ta = (utils.percentage(item['Tablet views'], item['Views']))
        fb = (utils.percentage(item['Fb refs'], item['Social refs']))
        tw = (utils.percentage(item['Tw refs'], item['Social refs']))
        inte = utils.humanize_number(item['Social interactions'], 1)

        text += f'''{rank}. {headline}
By {author} in {section}
VISITORS: {mv} min/visitor, visitors: {v}, returning: {r}%
TRAFFIC %: social {so}, search {se}, other {o}, direct {di}, internal {i}
SOCIAL BREAKDOWN %: FB {fb}, Twitter {tw} | Interactions: {inte}
DEVICES %: mobile {mo}, desktop {de}, tablet {ta}

-----------------------------------------------------------\n'''
    return text


def format_site(data, unit, ma):
    # data is a dict
    text = ''
    print(data['postv']['new'])
    if len(data['postv']['new']) > 6:
        a = (utils.humanize_number(data['postv']['new'], 1)).rjust(5)
    else:
        a = (utils.humanize_number(data['postv']['new'], 0)).rjust(5)
    b = (data['postv']['delta']).rjust(5)
    b2 = (data['postv']['kpi_delta']).rjust(5)
  
    c = (data['postv']['kpi_new']).ljust(4)
    if len(data['visitors']['new']) > 6:
        d = (utils.humanize_number(data['visitors']['new'], 1)).rjust(5)
    else:
        d = (utils.humanize_number(data['visitors']['new'], 0)).rjust(5)
    e = (data['visitors']['delta']).rjust(5)
    if len(data['minutes']['new']) > 6:
        f = (utils.humanize_number(data['minutes']['new'], 1)).rjust(5)
    else:
        f = (utils.humanize_number(data['minutes']['new'], 0)).rjust(5)
    g = (data['minutes']['delta']).rjust(5)
    g2 = (data['minutes']['kpi_new_ma_delta']).rjust(5)
    h = (data['minutes']['kpi_new']).ljust(4)
    i = utils.percentage(data['postv']['new'], data['pagev']['new'])
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
        ff = (utils.humanize_number(data['pagev']['new'], 1)).rjust(5)
    else:
        ff = (utils.humanize_number(data['pagev']['new'], 0)).rjust(5)
    gg = (data['pagev']['delta']).rjust(5)
    gg2 = (data['pagev']['kpi_delta']).rjust(5)
    hh = (data['pagev']['kpi_new']).ljust(4)
    if len(data['visitors']['new_pages']) > 6:
        ii = (utils.humanize_number(data['visitors']['new_pages'], 1)).rjust(5)
    else:
        ii = (utils.humanize_number(data['visitors']['new_pages'], 0)).rjust(5)
    jj = (data['visitors']['total_delta']).rjust(5)
    if len(data['minutes']['new_pages']) > 6:
        kk = (utils.humanize_number(data['minutes']['new_pages'], 1)).rjust(5)
    else:
        kk = (utils.humanize_number(data['minutes']['new_pages'], 0)).rjust(5)
    ll = (data['minutes']['total_delta']).rjust(5)
    ll2 = (data['minutes']['kpi_pages_ma_delta']).rjust(5)
    mm = (data['minutes']['kpi_pages']).ljust(4)
    oo = unit.ljust(5)
    text += f'''
===================================================
SITE            Last  |  vs  |  KPIs           vs
DETAILS:        {oo} |  MA% |                 MA%
---------------------------------------------------
Post views     {a}   {b}    {c}  v/vis. {b2}
Post visitors  {d}   {e}   -------------------
Post minutes   {f}   {g}    {h}  m/vis. {g2}
---------------------------------------------------
* Post views were {i}% of period's total page views
---------------------------------------------------
Page views     {ff}   {gg}    {hh}  v/vis. {gg2}
Page visitors  {ii}   {jj}   ------------------- 
Page minutes   {kk}   {ll}    {mm}  m/vis. {ll2}
===================================================
% POST     Last    M  |  VISITOR   Last    M
TRAFFIC:   {oo}   A  |  PROFILE:  {oo}   A
--------------------  |  -----------------------
Facebook     {j}   {k}  |  New         {l}   {m}
Twitter      {n}   {o}  |  Returning   {p}   {q}
Search       {r}   {s}  |  -----------------------
Other        {t}   {u}  |  DEVICES:
Direct       {v}   {w}  |  Mobile      {z}   {aa}
Internal     {x}   {y}  |  Desktop     {bb}   {cc}
                      |  Tablet      {dd}   {ee}
---------------------------------------------------
MA = moving average (prior 13 weeks)
Due to rounding, numbers may not add up to 100%
Google accounts for nearly all 'Search' views.
Google News, APIs account for most 'Other' views.
===================================================
'''
    return text


def format_data(data):
    text = ''
    text += f'''{data["report"].title()} web report: {data["site"].title()} for {data["report"].replace("daily", "").replace("ly", "")} {data["site_stats"]["date"]}''' + nl + nl
    text += dbl_line
    text += format_posts(data['posts_stats'])
    text += format_site(data['site_stats'], data['unit'], data['ma'])
    return text


def create_pdf(data):
    results = format_site(data['site_stats'], data['unit'], data['ma'])
    file_name = f'{data["report"]}_{data["site"].title()}_stats'

    # CREATE PDF
    # enscript -B -M A5 -p output.ps input.txt
    # ps2pdf output.ps output.pdf

    # subprocess.run(["ls", "-l"])  # doesn't capture output
    # save as text file. Note, this overwrites the file.
    with open(f'{file_name}.txt', "w") as f:
        f.write(results)

    subprocess.run(['/usr/local/bin/enscript', '-M', 'A5', '-p', f'{file_name}.ps', f'{file_name}.txt'])
    subprocess.run(['/usr/local/bin/ps2pdf', f'{file_name}.ps', f'{file_name}.pdf'])
