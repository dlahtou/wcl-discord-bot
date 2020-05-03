import requests
import urllib
import wcl_api.models as models
from properties import WARCRAFTLOGS_API_KEY
from wcl_api.scraper import get_parses
import pandas as pd

WARCRAFTLOGS_API_PATH = 'https://www.warcraftlogs.com:443/v1'
GUILD_PATH = WARCRAFTLOGS_API_PATH + '/reports/guild/{0}/{1}/{2}?api_key={3}'
FIGHTS_PATH = WARCRAFTLOGS_API_PATH + '/report/fights/{0}?api_key={1}'
OUT_FOLDER_PATH = '/DudesLogs/'


def get_newest_report_json(guild_name, server_name, server_region):
    reports = get_reports_json(guild_name, server_name, server_region)
    if len(reports) > 0:
        return reports[0]
    else:
        return {}


def get_reports_json(guild_name, server_name, server_region):
    guild_name = urllib.parse.quote(guild_name)
    r = requests.get(GUILD_PATH.format(guild_name, server_name, server_region, WARCRAFTLOGS_API_KEY))
    if r.status_code == 200:
        return r.json()
    else:
        return []


def get_fights_json(report):
    id_string = report.id_string
    zone_number = report.zone_number

    r = requests.get(FIGHTS_PATH.format(id_string, WARCRAFTLOGS_API_KEY))
    if r.status_code == 200:
        num_fights = len(r.json()['fights'])
        print('Found {0} fights!'.format(num_fights))
        return r.json()
    else:
        return {}

report = models.Report(get_newest_report_json('My Dudes', 'tichondrius', 'us'))
fights = models.Fights(get_fights_json(report))
parses = get_parses(report, fights)
print(len(parses))
highest_parse = None
for parse in parses:
    print(parse.ilvl_parse_percentile)
    
    if highest_parse is None or highest_parse.ilvl_parse_percentile < parse.ilvl_parse_percentile:
        highest_parse = parse
    
    print(highest_parse.character_name)
    print(highest_parse.ilvl_parse_percentile)
    print(highest_parse.boss_name)

parse_dicts = [parse.to_dict() for parse in parses]
df = pd.DataFrame(parse_dicts)
print(df.head(10))
df.to_csv(OUT_FOLDER_PATH + report.get_id_string() + '.csv')