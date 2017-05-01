import os
import time
from slackclient import SlackClient
from random import randint
from chatterbot import ChatBot
import urllib
from mtranslate import translate
import wikipedia

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
HIGHSCORE = 0;
# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "vlad"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


chatbot = ChatBot(
                  'Bot Botovich',
                  storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
                  logic_adapters=[
                                  "chatterbot.logic.MathematicalEvaluation",
                                  "chatterbot.logic.TimeLogicAdapter",
                                  "chatterbot.logic.BestMatch"
                                  ],
                  trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
                  filters=["chatterbot.filters.RepetitiveResponseFilter"],
                  database="../database.db"

                  )

# Train based on the english corpus
chatbot.train("chatterbot.corpus.english")






lang = ["af:", "sq:", "ar:", "az:", "eu:", "bn:", "be:", "bg:", "ca:", "zh-cn:", "zh-tw:",\
        "hr:", "cs:", "da:", "nl:", "en:", "eo:", "et:", "tl:", "fi:", "fr:", "gl:", "ka:",\
        "de:", "el:", "gu:", "ht:", "iw:", "hi:", "hu:", "is:", "id:", "ga:", "it:", "ja:",\
        "kn:", "ko:", "la:", "lv:", "lt:", "mk:", "ms:", "mt:", "no:", "fa:", "pl:", "pt:",\
        "ro:", "ru:", "sr:", "sk:", "sl:", "es:", "sw:", "sv:", "ta:", "te:", "th:", "tr:",\
        "uk:", "ur:", "vi:", "cy:", "yi:"]

wiki_liblang = ["af:", "sq:", "ar:", "az:", "eu:", "bn:", "be:", "bg:", "ca:", "zh:",\
                "hr:", "cs:", "da:", "nl:", "en:", "eo:", "et:", "tl:", "fi:", "fr:", "gl:", "ka:",\
                "de:", "el:", "gu:", "ht:", "iw:", "hi:", "hu:", "is:", "id:", "ga:", "it:", "ja:",\
                "kn:", "ko:", "la:", "lv:", "lt:", "mk:", "ms:", "mt:", "no:", "fa:", "pl:", "pt:",\
                "ro:", "ru:", "sr:", "sk:", "sl:", "es:", "sw:", "sv:", "ta:", "te:", "th:", "tr:",\
                "uk:", "ur:", "vi:", "cy:", "yi:"]

wiki_lang = ""
wiki_line = 1


def check_valid_lang(command):
    command = (command[10:len(command):] + ":").strip()
    for elem in wiki_liblang:
        if (elem == command):
            return True
    else:
        return False

def handle_translation(command):
    for elem in lang:
        if (command.startswith(elem)):
            to_translate = command[len(elem):len(command):].strip()
            origin = "auto"
            for elem2 in lang:
                if (to_translate.startswith(elem2)):
                    if (elem2 != "zh-cn:" and elem2 != "zh-tw:"):
                        origin = to_translate[0:2]
                    else:
                        origin = to_translate[0:5]
                    to_translate = to_translate[len(elem2):len(to_translate):]
            else:
                if (to_translate.startswith("auto:")):
                    to_translate = to_translate[len("auto:"):len(to_translate):]
            if (to_translate != "" and elem != "zh-cn:" and elem != "zh-tw:"):
                response = translate(to_translate.encode('utf-8'), elem[0:2:], origin)
            elif(to_translate != ""):
                if (elem == "zh-cn:"):
                    elem = "zh-CN:"
                else:
                    elem = "zh-TW:"
                response = translate(to_translate.encode('utf-8'), elem[0:5:], origin)
            else:
                response = "Nothing to translate"
            return response
    else:
        return ""

def find_definition(command):
    if(command.startswith("what is a ")):
        command = command[10:len(command)]
    elif (command.startswith("what is ") or command.startswith("who are ")):
        command = command[8:len(command)]
    elif (command.startswith("what are ") or command.startswith("what's a ")):
        command = command[9:len(command)]
    elif (command.startswith("who is ")):
        command = command[7:len(command)]
    elif (command.startswith("what's")):
        command = command[6:len(command)]
    if (command[len(command) - 1] == '?'):
        command = command[0:len(command) - 1]
    try:
        if (wiki_lang != ""):
            wikipedia.set_lang(wiki_lang[:-1])
            if (wiki_lang != "zh:"):
                lang = wiki_lang
            else:
                lang = "zh-cn:"
            command = command.strip()
            command = handle_translation(lang + command).lower()
        command = command.title()
        response = '```' + wikipedia.summary(command, sentences=wiki_line) + '```'
    except:
        response = "Need a clear one"
    return response



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




def handle_command(command, channel):
    response = ""
    command = command.strip()
    
    """global declaration"""
    
    global wiki_lang
    global wiki_line
    
    if command.startswith("wiki line:"):
        check_line = int(command[10:len(command):])
        if (check_line > 0 and check_line <= 100):
            wiki_line = int(command[10:len(command):].strip())
            response = "current wiki line is: *%d*" % wiki_line
        else:
            response = "`limit size 100`"
    if command.startswith("wiki lang:"):
        if (check_valid_lang(command)):
            wiki_lang = (command[10:len(command):] + ":").strip()
            response = "current wiki language is: *%s*" % wiki_lang[0:-1:]
        else:
            response = "`Invalid language`"
    if (handle_translation(command) != ""):
        response = "> *" + handle_translation(command) + "*"
    if (response != ""):
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        return
    
    """ here we translate the command to eng"""
    command = handle_translation(("en:" + command)).lower()
    char_replace = u"\u2019"
    command = command.replace(char_replace, "'")
    
    """check if it's a question """
    if command.startswith(("what's ", "what's a", "what is ",\
                           "what is a ", "what are ", "who is ", "who are ")):
        response = find_definition(command)
    elif command.startswith("wiki stat"):
        if (wiki_lang == ""):
            response = "current wiki lang is en\ncurrent wiki line is " + str(wiki_line)
        else:
            response = "current wiki lang is " + wiki_lang[:-1] + "\ncurrent wiki line is " + str(wiki_line)
    else:
            #response = "I don't understand"
            print("LoopMaker")
    if (response != ""):
            slack_client.api_call("chat.postMessage", channel=channel,
                    text=response, as_user=True)




    if command.startswith(EXAMPLE_COMMAND):
        if command.endswith("time") or command.endswith("Time"):
            timer()
        elif command.endswith("play_basketball") or command.endswith("random") or command.endswith("random_game"):
            
            randomBasketball()

        elif any(substring in command for substring in ["lawyer", "law", "legal", "airport"]):
            
            response = "Please refer to this group. (https://www.airportlawyer.org/)"
            slack_client.api_call("chat.postMessage", channel=channel,
                      text=response, as_user=True)
        elif any(substring in command for substring in ["visa", "H1" , "H-1" , "immigrate" , "Transfer"]):
            
            response = "I found a place where you can find help. (https://visabot.co/)"
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

        else:
            response = "Master i know not what you speak of!"
            # Get a response to an input statement
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    else:
        #response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
        "* command with numbers or words, delimited by spaces or _."
        print(command)
        response = str(chatbot.get_response(command))
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

