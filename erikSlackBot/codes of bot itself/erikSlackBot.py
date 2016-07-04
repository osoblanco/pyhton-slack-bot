import os
import time
from slackclient import SlackClient
from random import randint

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
HIGHSCORE = 0;
# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "jarvis_ask"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def randomBasketball():
    """
    writes down your basketball score
    """
    random = randint(0,100)
    
    global HIGHSCORE
    
    if random > HIGHSCORE :
        HIGHSCORE = random
        response = "You score is " + str(random) +" Congrats you set a new Highscore!!"
        slack_client.api_call("chat.postMessage", channel=channel,
                                  text=response, as_user=True)
    else:
        response = "You score is " + str(random) +". Highscore is " + str(HIGHSCORE) + "."
        slack_client.api_call("chat.postMessage", channel=channel,
                      text=response, as_user=True)





def timer():
    """
       writes down the current time for the user
        """
    response = "The time is " + time.strftime("%c")
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
        """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
        "* command with numbers, delimited by spaces."
    
    if command.startswith(EXAMPLE_COMMAND):
        if command.endswith("time") or command.endswith("Time"):
            timer()
        elif command.endswith("play_basketball") or command.endswith("random") or command.endswith("random_game"):
            randomBasketball()
        else:
            response = "Master i know not what you speak of!"
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    else:
        response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
        "* command with numbers or words, delimited by spaces or _."
        slack_client.api_call("chat.postMessage", channel=channel,
                      text=response, as_user=True)



def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

