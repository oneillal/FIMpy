from slacker import Slacker
from os import getenv

slack_token = getenv('SLACKTOKEN', 'xoxp-9999999999')

def alert_slack(file, host, ipaddress):
    slack = Slacker(slack_token)
    # Send a message to #general channel
    slack.chat.post_message('#alerts', '', 'FIMpy', 'false', '', '', '[{"color":"#FF0000","title":"FIMpy Alert","title_link":"https://' + host + '","text":"FIMpy has detected a potential integrity compromise with the following asset:","fields":[{"title":"Host (IP)","value":"' + host + ' (' + ipaddress + ')"},{"title":"File","value":"' + file + '"},{"title":"Type","value":"HMAC"}]}]', '', '', '', ':face-monkey:', '')