import os
import time
import re
import unicodedata
from slackclient import SlackClient
from bot import Bot

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# instantiate Slack client
slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_client = SlackClient(slack_token)
bot = Bot()

print('Your slack token is', slack_token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print(bcolors.OKGREEN, "DinnerBot status: running", bcolors.ENDC)
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        print(bcolors.OKGREEN, "DinnerBot id:", starterbot_id, bcolors.ENDC)
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                slack_client.api_call(
                    "chat.postMessage",
                    channel=channel,
                    text=bot.handle_command(command)
                )
            time.sleep(RTM_READ_DELAY)
    else:
        print(bcolors.FAIL ,"Connection failed. Exception traceback printed above.", bcolors.ENDC)
