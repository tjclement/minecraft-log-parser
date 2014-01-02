# -*- coding: utf-8 -*-

import re
import json
import requests
import datetime
import time
import mc_dynchat
import mc_datahandler
import mc_settings


commands = {
    "ping": re.compile("!ping"),
    "deaths_self": re.compile("!deaths"),
    "last_seen": re.compile("!lastseen (.*)"),
    "norris": re.compile("!norris")
}


def parse_chat_message(timestamp, user, message, user_data):
    threshold = datetime.datetime.now() - datetime.timedelta(seconds=5)

    if timestamp < threshold:
        return None

    for command in commands:
        if commands[command].match(message):
            command_name = "command_" + command
            method = getattr(mc_dynchat, command_name)
            if method is not None:
                method(user, message, user_data)
            else:
                print "Command %s is not implemented, but a chat regex was matched for it."
    return None


def command_ping(user, message, user_data):
    send_chat_message("Pong.")


def command_deaths_self(user, message, user_data):
    total_deaths = mc_datahandler.get_total_deaths(user, user_data)
    response = "User %(user)s died %(deaths)d times. Such a bad-ass." % {"user": user, "deaths": total_deaths}
    send_chat_message(response)


def command_last_seen(user, message, user_data):
    target = commands["last_seen"].split(message)[1]
    last_login = mc_datahandler.get_last_login(target, user_data)

    if last_login is None:
        send_chat_message("I don't know user %s, get him over here!" % target)
    else:
        last_logout = mc_datahandler.get_last_logout(target, user_data)

        if last_logout < last_login:
            send_chat_message("%s is still online, you silly goose!" % target)
        else:
            send_chat_message("I last saw %(target)s online at %(time)s. What a ninja!" % {"target": target, "time": last_logout})

def command_norris(user, message, user_data):
    response = requests.get("http://api.icndb.com/jokes/random")
    response = json.loads(response.text)
    joke = response["value"]["joke"]

    send_chat_message(joke)


def split_message(message):
    n = 94
    for start in range(0, len(message), n):
        yield message[start:start+n]


def send_chat_message(message):
    post_headers = {"Content-type": "application/json"}
    dynmap_send_uri = mc_settings.settings["dynmap_uri"] + "up/sendmessage"

    for text in split_message(message):
        text =  u'§b§l' + text
        post_data = {"message": text, "name": mc_settings.settings["chat_name"]}
        r = requests.post(dynmap_send_uri, data=json.dumps(post_data),
                        headers=post_headers, verify=mc_settings.settings["verify_ssl"])
        time.sleep(6)