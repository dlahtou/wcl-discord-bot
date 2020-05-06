from selenium.webdriver.common.by import By
from wcl_api.util import parse_int_else_zero
import re

zones_dict = {
    24: "Ny'alotha"
}

thumbs_by_zone = {
    24: 'https://dmszsuqyoe6y6.cloudfront.net/img/warcraft/zones/zone-24.png'
}

raider_io_zones_dict = {
    24: 'nyalotha-the-waking-city'
}

role_dict = {
    'Blood': 'tank',
    'Frost': 'damage',
    'Unholy': 'damage',
    'Havoc': 'damage',
    'Vengeance': 'tank',
    'Balance': 'damage',
    'Feral': 'damage',
    'Restoration': 'healer',
    'Guardian': 'tank',
    'BeastMastery': 'damage',
    'Marksmanship': 'damage',
    'Survival': 'damage',
    'Arcane': 'damage',
    'Fire': 'damage',
    'Brewmaster': 'tank',
    'Mistweaver': 'healer',
    'Windwalker': 'damage',
    'Holy': 'healer',
    'Protection': 'tank',
    'Retribution': 'damage',
    'Discipline': 'healer',
    'Shadow': 'damage',
    'Assassination': 'damage',
    'Outlaw': 'damage',
    'Subtlety': 'damage',
    'Elemental': 'damage',
    'Enhancement': 'damage',
    'Affliction': 'damage',
    'Demonology': 'damage',
    'Destruction': 'damage',
    'Arms': 'damage',
    'Fury': 'damage',
    'unknown': 'unknown'
}

difficulty_dict = {
    5: 'Mythic',
    4: 'Heroic',
    3: 'Normal',
    2: 'Normal',
    1: 'Normal'
}

class Fights:
    def __init__(self, wcl_json):
        self.fights = wcl_json['fights']
        self.friendlies = wcl_json['friendlies']
        self.title = wcl_json['title']
        self.zone_number = wcl_json['zone']
        self.difficulty = difficulty_dict[wcl_json['fights'][0]['difficulty']]

        if wcl_json['zone'] in wcl_json.keys():
            self.zone_name = zones_dict[self.zone_number]
        else:
            self.zone_name = 'unknown'

        self.start_time_epoch_millis = wcl_json['start']

        self.kills = []
        for fight in self.fights:
            if fight['boss'] != 0 and fight['kill'] == True:
                self.kills.append(fight)

    def get_kill_ids(self):
        fight_ids = []

        for fight in self.kills:
            fight_ids.append(fight['id'])

        return fight_ids

    def get_kill_boss_names(self):
        fight_boss_names = []

        for fight in self.kills:
            fight_boss_names.append(fight['name'])

        return fight_boss_names

class Report:
    def __init__(self, wcl_json):
        self.id_string = wcl_json['id']
        self.title = wcl_json['title']
        self.owner = wcl_json['owner']
        self.start_time_epoch_millis = wcl_json['start']
        self.end_time_epoch_millis = wcl_json['end']
        self.zone_number = wcl_json['zone']
        self.zone_name = zones_dict[self.zone_number]
        self.zone_thumb = thumbs_by_zone[self.zone_number] if self.zone_number in thumbs_by_zone.keys() else ''
        self.url = 'https://www.warcraftlogs.com/reports/{0}'.format(self.id_string)
    
    def get_zone_number(self):
        return self.zone_number
    
    def get_id_string(self):
        return self.id_string

    def get_formatted_duration(self):
        duration_total = (self.end_time_epoch_millis - self.start_time_epoch_millis)//1000 #seconds
        
        duration_hours = duration_total//3600
        duration_minutes = (duration_total % 3600)//60
        duration_seconds = duration_total % 60

        return ':'.join([str(duration_hours), f'{duration_minutes:02}', f'{duration_seconds:02}'])

class Parse:
    def __init__(self, fight, row, parse_type):
        #expects a selenium WebElement for row
        self.boss_name = fight['name']
        self.difficulty = difficulty_dict[fight['difficulty']]
        self.parse_type = parse_type
        self.ilvl = parse_int_else_zero(row.find_element(By.CSS_SELECTOR, '.main-table-number.main-table-ilvl').get_attribute('innerHTML'))
        
        class_and_spec_icon = row.find_element(By.CSS_SELECTOR, '.report-table-icon')
        icon_css_classnames = class_and_spec_icon.get_attribute("class").split(' ')
        self.class_name = 'unknown'
        self.spec_name = 'unknown'
        for css_classname in icon_css_classnames:
            if re.match('actor-sprite-', css_classname):
                self.class_name = css_classname.split('-')[2]
                self.spec_name = css_classname.split('-')[3]

        self.role = role_dict[self.spec_name]
        
        overall_parse_a = row.find_element(By.CSS_SELECTOR, '.main-table-performance.rank > a')
        self.overall_parse_rarity = overall_parse_a.get_attribute('class')
        self.overall_parse_percentile = parse_int_else_zero(overall_parse_a.get_attribute('innerHTML'))
        
        self.character_name = row.find_element(By.CSS_SELECTOR, '.main-table-name.report-table-name a').get_attribute('innerHTML').strip()
        self.total = parse_int_else_zero(row.find_element(By.CSS_SELECTOR, '.report-table-amount.main-table-amount span').get_attribute('innerHTML'))
        self.per_second_amount = parse_int_else_zero(row.find_element(By.CSS_SELECTOR, '.main-table-number.main-per-second-amount').get_attribute('innerHTML').split('.')[0])
        
        ilvl_parse_a = row.find_element(By.CSS_SELECTOR, '.main-table-ilvl-performance.rank > a')
        self.ilvl_parse_rarity = ilvl_parse_a.get_attribute('class')
        self.ilvl_parse_percentile = parse_int_else_zero(ilvl_parse_a.get_attribute('innerHTML'))

    def to_dict(self):
        return {
            'difficulty': self.difficulty,
            'boss_name': self.boss_name,
            'parse_type': self.parse_type,
            'character_name': self.character_name,
            'ilvl': self.ilvl,
            'spec_name': self.spec_name,
            'class_name': self.class_name,
            'role': self.role,
            'overall_parse_rarity': self.overall_parse_rarity,
            'overall_parse_percentile': self.overall_parse_percentile,
            'total': self.total,
            'per_second_amount': self.per_second_amount,
            'ilvl_parse_rarity': self.ilvl_parse_rarity,
            'ilvl_parse_percentile': self.ilvl_parse_percentile
        }

class Raider_IO:
    def __init__(self, raider_io_rankings_json, raider_io_progression_json):
        self.guild_name = raider_io_rankings_json['name']
        self.faction = raider_io_rankings_json['faction']
        self.region = raider_io_rankings_json['region']
        self.realm = raider_io_rankings_json['realm']
        self.profile_url = raider_io_rankings_json['profile_url']
        self.raid_rankings = raider_io_rankings_json['raid_rankings']
        self.raid_progression = raider_io_progression_json['raid_progression']


class Ranking:
    def __init__(self, parent_json, zone_id, difficulty):
        json = parent_json[raider_io_zones_dict[zone_id]][difficulty]
        self.world = json['world']
        self.region = json['region']
        self.realm = json['realm']


class Progression:
    def __init__(self, parent_json, zone_id):
        json = parent_json[raider_io_zones_dict[zone_id]]
        self.num_bosses = json['total_bosses']
        self.normal_int = json['normal_bosses_killed']
        self.heroic_int = json['heroic_bosses_killed']
        self.mythic_int = json['mythic_bosses_killed']
        self.normal_string = '{0}/{1}'.format(self.normal_int, self.num_bosses)
        self.heroic_string = '{0}/{1}'.format(self.heroic_int, self.num_bosses)
        self.mythic_string = '{0}/{1}'.format(self.mythic_int, self.num_bosses)