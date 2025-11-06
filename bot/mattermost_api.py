import os
import requests

MATTERMOST_TOKEN = os.environ.get('MATTERMOST_TOKEN')
MATTERMOST_URL = os.environ.get('MATTERMOST_URL')

class MattermostAPI:
    def __init__(self):
        self.token = MATTERMOST_TOKEN
        self.url = MATTERMOST_URL
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def post_message(self, channel_id, message):
        endpoint = f"{self.url}/api/v4/posts"
        data = {
            "channel_id": channel_id,
            "message": message
        }
        resp = requests.post(endpoint, json=data, headers=self.headers)
        return resp.json()
