import os
import requests

LINEAR_API_TOKEN = os.environ.get('LINEAR_API_TOKEN')
LINEAR_API_URL = 'https://api.linear.app/graphql'

class LinearAPI:
    def __init__(self):
        self.token = LINEAR_API_TOKEN
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def create_issue(self, team_id, title, description):
        query = '''mutation IssueCreate($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                issue { id title url }
            }
        }'''
        variables = {
            "input": {
                "teamId": team_id,
                "title": title,
                "description": description
            }
        }
        resp = requests.post(LINEAR_API_URL, json={"query": query, "variables": variables}, headers=self.headers)
        return resp.json()

    def list_issues(self, team_id, status):
        query = '''query Issues($filter: IssueFilter) {
            issues(filter: $filter) {
                nodes { id title url state }
            }
        }'''
        variables = {
            "filter": {
                "team": {"id": team_id},
                "state": status
            }
        }
        resp = requests.post(LINEAR_API_URL, json={"query": query, "variables": variables}, headers=self.headers)
        return resp.json()
