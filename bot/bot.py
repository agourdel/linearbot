
import os
from errbot import BotPlugin, arg_botcmd
from flask import Flask, request
from config import ConfigManager
from linear_api import LinearAPI
from mattermost_api import MattermostAPI

app = Flask(__name__)
config_mgr = ConfigManager()
linear_api = LinearAPI()
mm_api = MattermostAPI()

class LinearBot(BotPlugin):
    @arg_botcmd('linear_team', type=str)
    def set_team(self, msg, linear_team=None):
        mattermost_team = msg.to.group
        config_mgr.set_team_mapping(mattermost_team, linear_team)
        return f"Team mapping saved: {mattermost_team} -> {linear_team}"

    @arg_botcmd('title', type=str)
    @arg_botcmd('body', type=str)
    def create(self, msg, title=None, body=None):
        mattermost_team = msg.to.group
        linear_team = config_mgr.get_linear_team(mattermost_team)
        if not linear_team:
            return "No Linear team mapped. Use /linear set-team first."
        # Détermination du corps de l'issue selon le contexte
        issue_body = body or ""
        # Si le message cite un autre message
        if hasattr(msg, 'extras') and msg.extras.get('quoted_message'):  # ErrBot extras
            issue_body = msg.extras['quoted_message']
        # Si le message est dans un fil de discussion (topic)
        elif hasattr(msg, 'thread_id') and msg.thread_id:
            # Ici, il faudrait récupérer tous les messages du fil
            # (pseudo-code, dépend de l'intégration Mattermost/ErrBot)
            # issue_body = get_thread_messages(msg.thread_id)
            issue_body = f"[Thread] {body}"
        # Si rien, on prend le texte direct
        elif not issue_body:
            issue_body = msg.body
        # TODO: Get Linear team ID from name (requires API call)
        team_id = linear_team # Simplification, replace with actual lookup
        result = linear_api.create_issue(team_id, title, issue_body)
        try:
            url = result['data']['issueCreate']['issue']['url']
            return f"Issue '{title}' created: {url}"
        except Exception:
            return f"Error creating issue: {result}"

    @arg_botcmd('status', type=str)
    def list(self, msg, status=None):
        mattermost_team = msg.to.group
        linear_team = config_mgr.get_linear_team(mattermost_team)
        if not linear_team:
            return "No Linear team mapped. Use /linear set-team first."
        team_id = linear_team # Simplification, replace with actual lookup
        result = linear_api.list_issues(team_id, status)
        try:
            issues = result['data']['issues']['nodes']
            return '\n'.join([f"{i['title']}: {i['url']} [{i['state']}]" for i in issues])
        except Exception:
            return f"Error listing issues: {result}"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Example: {'teamId': '...', 'issue': {'title': '...', 'url': '...', 'state': '...'}}
    team_id = data.get('teamId')
    issue = data.get('issue')
    # Find corresponding Mattermost team
    for mm_team, lin_team in config_mgr.data.items():
        if lin_team == team_id:
            # Post update to Mattermost (channel_id should be mapped/configured)
            mm_api.post_message(mm_team, f"Update: {issue['title']} is now {issue['state']} {issue['url']}")
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
