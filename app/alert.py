from slacker import Slacker

def alert_slack(file, host, ipaddress):
    CONFIG = []
    slack = Slacker(CONFIG['slack_token'])
    # Send a message to #general channel
    slack.chat.post_message('#alerts', '', 'FIMpy', 'false', '', '', '[{"color":"#FF0000","title":"FIMpy Alert","title_link":"https://' + host + '","text":"FIMpy has detected a potential integrity compromise with the following asset:","fields":[{"title":"Host (IP)","value":"' + host + ' (' + ipaddress + ')"},{"title":"File","value":"' + file + '"},{"title":"Type","value":"HMAC"}]}]', '', '', '', ':face-monkey:', '')