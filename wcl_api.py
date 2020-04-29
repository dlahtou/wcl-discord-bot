import requests
import urllib

PUBLIC_KEY = 'bb7a652ddabff076285430d88b002dc8'
WARCRAFTLOGS_API_PATH = 'https://www.warcraftlogs.com:443/v1/'
GUILD_PATH = WARCRAFTLOGS_API_PATH + 'reports/guild/{0}/{1}/{2}?api_key={3}'
REPORT_PATH = WARCRAFTLOGS_API_PATH + '/report/fights/{0}'

def get_newest_report_fights(guildName, serverName, serverRegion):
    reports = get_reports(guildName, serverName, serverRegion)
    if len(reports) > 0:
        return reports[0]
    else:
        return {}

def get_reports(guildName, serverName, serverRegion):
    guildName = urllib.parse.quote(guildName)
    r = requests.get(GUILD_PATH.format(guildName, serverName, serverRegion, PUBLIC_KEY))
    if r.status_code == 200:
        return r.json()
    else:
        return []

get_newest_report('My Dudes', 'tichondrius', 'us')