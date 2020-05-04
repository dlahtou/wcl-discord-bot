import requests
import urllib

RAIDER_IO_RANKINGS_API_URL = 'https://raider.io/api/v1/guilds/profile?region={0}&realm={1}&name={2}&fields=raid_rankings'
RAIDER_IO_PROGRESSION_API_URL = 'https://raider.io/api/v1/guilds/profile?region={0}&realm={1}&name={2}&fields=raid_progression'

def get_rankings_json(guild_name, realm_name, server_region):
    guild_name = urllib.parse.quote(guild_name)
    r = requests.get(RAIDER_IO_RANKINGS_API_URL.format(server_region, realm_name, guild_name))
    if r.status_code == 200:
        return r.json()
    else:
        print(r.status_code)
        print('unable to access raider IO api')
        return {}

def get_progression_json(guild_name, realm_name, server_region):
    guild_name = urllib.parse.quote(guild_name)
    r = requests.get(RAIDER_IO_PROGRESSION_API_URL.format(server_region, realm_name, guild_name))
    if r.status_code == 200:
        return r.json()
    else:
        print(r.status_code)
        print('unable to access raider IO api')
        return {}