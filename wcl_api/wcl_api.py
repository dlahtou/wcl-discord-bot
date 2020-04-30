import requests
import urllib
import wcl_api.models as models
from properties import WARCRAFTLOGS_API_KEY

WARCRAFTLOGS_API_PATH = 'https://www.warcraftlogs.com:443/v1'
GUILD_PATH = WARCRAFTLOGS_API_PATH + '/reports/guild/{0}/{1}/{2}?api_key={3}'
FIGHTS_PATH = WARCRAFTLOGS_API_PATH + '/report/fights/{0}?api_key={1}'


def get_newest_report(guild_name, server_name, server_region):
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
    id_string = report['id']
    zone_number = report['zone']

    r = requests.get(FIGHTS_PATH.format(id_string, WARCRAFTLOGS_API_KEY))
    if r.status_code == 200:
        num_fights = len(r.json()['fights'])
        print('Found {0} fights!'.format(num_fights))
        return r.json()
    else:
        return {}

report = get_newest_report('My Dudes', 'tichondrius', 'us')
fights = models.Fights(get_fights_json(report))
print(fights.get_kill_ids())
print(fights.get_kill_boss_names())
