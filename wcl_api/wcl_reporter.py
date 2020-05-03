from wcl_api import wcl_api, models, scraper
from os.path import join, isfile
from os import getcwd, remove
import pandas as pd
from datetime import date

PARENT_OUT_FOLDER = 'DudesLogs'
REPORT_FOLDER = 'reports'

def get_report_dataframe(report, fights):
    filename = join(getcwd(), OUT_FOLDER_NAME, report.get_id_string() + '.csv')

    df = None
    if isfile(filename):
        print("Loading report data from file")
        df = pd.read_csv(filename)
    else:
        print("Scraping warcraftlogs for report data")
        parses = scraper.get_parses(report, fights)

        parse_dicts = [parse.to_dict() for parse in parses]
        df = pd.DataFrame(parse_dicts)
        df.to_csv(filename)
        print("Scrape complete. Saving csv.")

    return df

def build_report(report, fights, df):
    filename = join(getcwd(), PARENT_OUT_FOLDER, REPORT_FOLDER, report.id_string + '.txt')
    if not isfile(filename):
        with open(filename, 'w') as open_file:
            lines = []
            lines.append('```')
            lines.append('{0} {1} {2}'.format(fights.difficulty, report.zone_name, format_date(report.start_time_epoch_millis)))
            lines.append('============================================')
            lines.append('Raid Duration: {0}'.format(report.get_formatted_duration()))
            lines.append('Bosses Down: {0}'.format(len(fights.kills)))
            lines.append('Wipes: {0} total'.format(len(fights.fights) - len(fights.kills)))
            lines.append('')
            lines.append('TONIGHT\'S TOP FIGHT:')
            lines.append(get_top_fight_string(df))
            lines.append('')
            lines.append('TOP ILVL DPS PERFORMANCES:')
            lines += get_top_ilvl_dps_performances(df)
            lines.append('')
            lines.append('TOP SPEC-WIDE DPS PERFORMANCES:')
            lines += get_top_overall_dps_performances(df)
            lines.append('')
            lines.append('BEST HPS (SINGLE FIGHT):')
            lines += get_top_hps(df)
            lines.append('```')

            open_file.writelines(line + '\n' for line in lines)

    with open(filename) as open_file:
        text = open_file.read()
    
    return text

def report():
    report = models.Report(wcl_api.get_newest_report_json('My Dudes', 'tichondrius', 'us'))
    fights = models.Fights(wcl_api.get_fights_json(report))
    df = get_report_dataframe(report, fights)

    return build_report(report, fights, df)


def format_date(start_time_epoch_millis):
    return date.fromtimestamp(start_time_epoch_millis//1000).strftime("%A %m/%d/%y")


def get_damage_only_dataframe(df):
    return df[(df.parse_type == 'damage-done') & (df.role == 'damage')]


def get_heal_only_dataframe(df):
    return df[(df.parse_type == 'healing') & (df.role == 'healer')]


def get_top_fight_string(df):
    averaged_parses_series = get_damage_only_dataframe(df).groupby(['difficulty', 'boss_name'])['ilvl_parse_percentile'].mean()
    difficulty = averaged_parses_series.idxmax()[0]
    boss_name = averaged_parses_series.idxmax()[1]
    average_parse = averaged_parses_series.max()
    return '{0} {1}: {2} raid average ilvl parse'.format(difficulty[0], boss_name, average_parse)


def get_top_ilvl_dps_performances(df):
    num_rows = 10
    damage_parses = get_damage_only_dataframe(df)

    top10tuples = damage_parses.sort_values('ilvl_parse_percentile', ascending=False).head(num_rows).reset_index(drop=True)

    formatted_parse_strings = []

    for i in range(num_rows):
        row = top10tuples.iloc[i]
        formatted_parse_strings.append(parse_performance_line(row, i+1, 'ilvl_parse_percentile'))

    return formatted_parse_strings

def get_top_overall_dps_performances(df):
    num_rows = 5
    damage_parses = get_damage_only_dataframe(df)

    top10tuples = damage_parses.sort_values('overall_parse_percentile', ascending=False).head(num_rows).reset_index(drop=True)

    formatted_parse_strings = []

    for i in range(num_rows):
        row = top10tuples.iloc[i]
        formatted_parse_strings.append(parse_performance_line(row, i+1, 'overall_parse_percentile'))

    return formatted_parse_strings

def get_top_hps(df):
    num_rows = 5
    damage_parses = get_heal_only_dataframe(df)

    top10tuples = damage_parses.sort_values('per_second_amount', ascending=False).head(num_rows).reset_index(drop=True)

    formatted_parse_strings = []

    for i in range(num_rows):
        row = top10tuples.iloc[i]
        formatted_parse_strings.append(parse_performance_line(row, i+1, 'overall_parse_percentile'))

    return formatted_parse_strings

def parse_performance_line(parse_row, i, percentile_type):
    character_name = parse_row['character_name']
    percentile = parse_row[percentile_type]

    per_second_amount = parse_row['per_second_amount']
    per_second_units = 'DPS' if parse_row['parse_type'] == 'damage-done' else 'HPS'
    per_second_string = '{0:>4}k  {1}'.format(round(per_second_amount/1000, 1), per_second_units)

    difficulty = parse_row['difficulty'][0]
    boss_name = parse_row['boss_name']

    return '{0}.) ({1}) {2:<12} -- {3} ({4} {5})'.format(i, percentile, character_name, per_second_string, difficulty, boss_name)





