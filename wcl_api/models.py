from selenium.webdriver.common.by import By
from wcl_api.util import parse_int_else_zero

zones_dict = {
    24: "Ny'alotha"
}

class Fights:
    def __init__(self, wcl_json):
        self.fights = wcl_json['fights']
        self.friendlies = wcl_json['friendlies']
        self.title = wcl_json['title']
        self.zone_number = wcl_json['zone']

        if wcl_json['zone'] in wcl_json.keys():
            self.zone_name = zones_dict[self.zone_number]
        else:
            self.zone_name = 'unknown'

        self.start_time_epoch_millis = wcl_json['start']

        self.kills = []
        for fight in self.fights:
            if fight['kill'] == True:
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
    
    def get_zone_number(self):
        return self.zone_number
    
    def get_id_string(self):
        return self.id_string

class Parse:
    def __init__(self, fight, row, parse_type):
        #expects a selenium WebElement for row
        self.boss_name = fight['name']
        self.parse_type = parse_type
        
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
            'boss_name': self.boss_name,
            'parse_type': self.parse_type,
            'overall_parse_rarity': self.overall_parse_rarity,
            'overall_parse_percentile': self.overall_parse_percentile,
            'character_name': self.character_name,
            'total': self.total,
            'per_second_amount': self.per_second_amount,
            'ilvl_parse_rarity': self.ilvl_parse_rarity,
            'ilvl_parse_percentile': self.ilvl_parse_percentile
        }