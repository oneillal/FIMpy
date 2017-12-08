#!/usr/bin/env python
"""
FIMpy - A Python File Integrity Monitoring Application
"""

#########################################################################################
###################################  ALERT  #############################################
#########################################################################################
#                                                                                       #
#   Python module for alert functions. MVP only contains logging and push notifications #
#   via Slack                                                                           #
#                                                                                       #
#########################################################################################

__author__ = "Alan O'Neill"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Alan O'Neill"
__status__ = "Development"

from slacker import Slacker
from os import getenv

# Get slack toekn from ENV
slack_token = getenv('SLACKTOKEN', 'xoxp-9999999999')

def alert_slack(doc, host, ipaddress):
    slack = Slacker(slack_token)
    # Send a message to #general channel
    slack.chat.post_message('#alerts', '', 'FIMpy', 'false', '', '', '[{"color":"#FF0000","title":"FIMpy Alert","title_link":"https://' + host + '","text":"FIMpy has detected a potential integrity compromise with the following asset:","fields":[{"title":"Host (IP)","value":"' + host + ' (' + ipaddress + ')"},{"title":"File","value":"' + doc + '"},{"title":"Type","value":"HMAC"}]}]', '', '', '', ':face-monkey:', '')