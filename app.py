import pyperclip
import sys
import utils as utl
import config as cfg


# from pprint import pprint

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

if len(sys.argv) > 2 and (sys.argv)[1] in ['daily', 'weekly', 'monthly'] and (sys.argv)[2] in ['spectator', 'record', 'niagara', 'standard', 'examiner', 'tribune', 'review', 'star']:
    freq = (sys.argv)[1]
    site = (sys.argv)[2]
else:
    print("Requires 2 parameters:\n[daily/weekly/monthly]\n[spectator/record/niagara/examiner/star]")
    sys.exit()
print('format is: ', freq)
if freq == 'daily':
    import format_daily as fmt
if freq == 'weekly':
    import format_weekly as fmt
if freq == 'monthly':
    import format_monthly as fmt

# print('Frequency is: ', freq)
# print("Site is: ", site)

stats_file_path = f'data_in/{freq}/' + cfg.files[site][freq]['stats']
posts_file_path = f'data_in/{freq}/' + cfg.files[site][freq]['posts']

# MAIN

data = utl.process_csv(stats_file_path, freq, site)
data['posts_stats'] = (utl.return_csv(posts_file_path))[cfg.slice_var[freq]]
# -- data = utl.site_stats(stats_values, ma_values, ma_units)
# pprint(data)
results = fmt.format_data(data)
fmt.create_pdf(data)
print(results)

# --- s = fmt.format_data(data)

# print(s)
# pprint.pprint(posts_values)
pyperclip.copy(results)

# save as text file. Note, this overwrites the file.
with open(f"data_reports/{freq}_{site}.txt", "w") as f:
    f.write(results)
