import os
import json

CONFIG_PATH = os.environ.get('LINEARBOT_CONFIG_PATH', '/tmp/linearbot_config.json')

class ConfigManager:
    def __init__(self):
        self.path = CONFIG_PATH
        self.data = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def set_team_mapping(self, mattermost_team, linear_team):
        self.data[mattermost_team] = linear_team
        self.save()

    def get_linear_team(self, mattermost_team):
        return self.data.get(mattermost_team)
