from wcl_api import wcl_api, models, scraper
from wcl_api import raider_io_api
from os.path import join, isfile, isdir
from os import getcwd, mkdir
import pandas as pd
from datetime import date
from discord import Embed, Colour
import json

PARENT_OUT_FOLDER = 'DudesLogs'
REPORT_FOLDER = 'reports'

def get_report_dataframe(report, fights):
    filename = join(getcwd(), PARENT_OUT_FOLDER, report.get_id_string() + '.csv')

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

def build_report(report, fights, df, raider_io_rankings):
    filename = join(getcwd(), PARENT_OUT_FOLDER, REPORT_FOLDER, report.id_string + '.json')
    if not isfile(filename):
        embed = Embed()
        embed.title = 'My Dudes {0} {1} ({2})'.format(fights.difficulty, report.zone_name, format_date(report.start_time_epoch_millis))
        embed.color = Colour.gold()
        embed.set_thumbnail(url=report.zone_thumb)
        embed.description = '[View on Warcraft Logs]({0})'.format(report.url)
        embed.add_field(name='Raid Duration', value=report.get_formatted_duration())
        embed.add_field(name='Bosses Down', value=len(fights.kills))
        embed.add_field(name='Wipes', value=(len(fights.fights) - len(fights.kills)))
        embed.add_field(name='Top Fight', value=get_top_fight_string(df), inline=False)
        embed.add_field(name='Top DPS', value=get_best_ilvl_performer(df), inline=False)

        embed.add_field(name='ilvl DPS', value='\n'.join([x.split(' -- ')[0] for x in get_top_ilvl_dps_performances(df)]), inline=True)
        embed.add_field(name='\u200b', value='\n'.join([x.split(' -- ')[1] for x in get_top_ilvl_dps_performances(df)]), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)

        embed.add_field(name='Spec-wide DPS', value='\n'.join([x.split(' -- ')[0] for x in get_top_overall_dps_performances(df)]), inline=True)
        embed.add_field(name='\u200b', value='\n'.join([x.split(' -- ')[1] for x in get_top_overall_dps_performances(df)]), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)

        embed.add_field(name='HPS', value='\n'.join([x.split(' -- ')[0] for x in get_top_hps(df)]), inline=True)
        embed.add_field(name='\u200b', value='\n'.join([x.split(' -- ')[1] for x in get_top_hps(df)]), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)

        embed.set_footer(text=build_footer_text(report, raider_io_rankings))

        print('Writing new report embed to file...')
        with open(filename, 'w') as open_file:
            open_file.write(json.dumps(embed.to_dict()))

    with open(filename) as open_file:
        print('Returning embed from file...')
        return Embed.from_dict(json.load(open_file))


def report():
    report = models.Report(wcl_api.get_newest_report_json('My Dudes', 'tichondrius', 'us'))
    fights = models.Fights(wcl_api.get_fights_json(report))
    prep_folders()
    df = get_report_dataframe(report, fights)
    raider_io_rankings = models.Raider_IO(raider_io_api.get_rankings_json('My Dudes', 'tichondrius', 'us'), raider_io_api.get_progression_json('My Dudes', 'tichondrius', 'us'))

    return build_report(report, fights, df, raider_io_rankings)


def prep_folders():
    if not isdir(PARENT_OUT_FOLDER):
        mkdir(PARENT_OUT_FOLDER)
    if not isdir(join(PARENT_OUT_FOLDER, REPORT_FOLDER)):
        mkdir(join(PARENT_OUT_FOLDER, REPORT_FOLDER))

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
    return '**{0} {1}**: {2} raid average ilvl parse'.format(difficulty[0], boss_name, average_parse)


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

    return '({1}) **{2}** -- {3} ({4} {5})'.format(i, percentile, character_name, per_second_string, difficulty, boss_name)

def get_best_ilvl_performer(df):
    num_rows = 10
    damage_parses = get_damage_only_dataframe(df)

    averaged_parses_series = damage_parses.groupby(['character_name'])['overall_parse_percentile'].mean()
    character_name = averaged_parses_series.idxmax()
    average_parse = averaged_parses_series.max()

    return '**{0}**: {1:.2f} average overall parse'.format(character_name, average_parse)


def build_footer_text(report, rio):
    rankings_json = rio.raid_rankings
    normal_rankings = models.Ranking(rankings_json, report.zone_number, 'normal')
    heroic_rankings = models.Ranking(rankings_json, report.zone_number, 'heroic')
    mythic_rankings = models.Ranking(rankings_json, report.zone_number, 'mythic')
    progression = models.Progression(rio.raid_progression, report.zone_number)
    footer_text = ['Rankings for {0} ({1}-{2}) via Raider.IO:'.format(rio.guild_name, rio.region.upper(), rio.realm)]
    if normal_rankings.realm > 0:
        footer_text.append('Normal Difficulty ({0}): #{1} World (#{2} Realm)'.format(progression.normal_string, normal_rankings.world, normal_rankings.realm))
    if heroic_rankings.realm > 0:
        footer_text.append('Heroic Difficulty ({0}): #{1} World (#{2} Realm)'.format(progression.heroic_string, heroic_rankings.world, heroic_rankings.realm))
    if mythic_rankings.realm > 0:
        footer_text.append('Mythic Difficulty ({0}): #{1} World (#{2} Realm)'.format(progression.mythic_string, mythic_rankings.world, mythic_rankings.realm))

    return '\n'.join(footer_text)