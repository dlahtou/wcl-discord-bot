class Fights:
    zones_dict = {
        24: "Ny'alotha"
    }

    def __init__(self, wcl_json):
        self.fights = wcl_json['fights']
        self.friendlies = wcl_json['friendlies']
        self.title = wcl_json['title']

        if wcl_json['zone'] in wcl_json.keys():
            self.zone = zones_dict[wcl_json['zone']]
        else:
            self.zone = 'unknown'

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