import re
import json
import requests
import datetime
import mc_dynchat
import mc_datahandler
import mc_settings


commands = {
    "deaths_self": re.compile("!deaths"),
    "lastseen": re.compile("!lastseen (.*)")
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


def command_deaths_self(user, message, user_data):
    total_deaths = mc_datahandler.get_total_deaths(user, user_data)
    response = "User %(user)s died %(deaths)d times. Such a bad-ass." % {"user": user, "deaths": total_deaths}
    send_chat_message(response)


def send_chat_message(message):
    post_headers = {"Content-type": "application/json"}
    post_data = {"message": message, "name": mc_settings.settings["chat_name"]}
    dynmap_send_uri = mc_settings.settings["dynmap_uri"] + "up/sendmessage"

    r = requests.post(dynmap_send_uri, data=json.dumps(post_data),
                        headers=post_headers, verify=mc_settings.settings["verify_ssl"])