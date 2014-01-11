import re
import datetime
import mc_dynchat

DATETIME = "([0-9]{4})\-([0-9]{2})\-([0-9]{2}) ([0-2][0-9])\:([0-9]{2})\:([0-9]{2}) ";

actions = {
    "login": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) ?\[\/[0-9.]{4,15}\:[0-9]*\]"),
    "logout": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) lost connection"),
    "server_stop": re.compile(DATETIME + "\[INFO\] Stopping server"),
    "server_start": re.compile(DATETIME + "\[INFO\] Starting minecraft server"),
    "server_name": re.compile(DATETIME + "\[INFO\] Preparing level \"(.*)\""),
    "blown_up": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was blown up by (.*)"),
    "shot": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was shot by (.*)"),
    "slain": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was slain by (.*)"),
    "burnt_by": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was burnt to a crisp whilst fighting (.*)"),
    "lava": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) tried to swim in lava"),
    "inflames": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) went up in flames"),
    "fell": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) fell from a high place"),
    "pricked": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was pricked to death"),
    "fell_by": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was doomed to fall by (.*)"),
    "drowned": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) drowned"),
    "suffocated": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) suffocated in a wall"),
    "chat_message": re.compile(DATETIME + "\[INFO\] \<(.*)\> (.*)"),
    "web_chat_message": re.compile(DATETIME + "\[INFO\] \[Dynmap\] \[WEB\] (.*): (.*)")
}

data = {}
server_name = ""


def parse_time(regexresult):
    time = datetime.datetime(int(regexresult[1]), int(regexresult[2]), int(regexresult[3]),
                                    int(regexresult[4]), int(regexresult[5]), int(regexresult[6]))
    return time


def handle_user(user):
    if user not in data:
        data[user] = {}
    return None


def add_user_time(user, stop_time):
    if "currentlogintimestamp" in data[user]:
        online_time = stop_time - data[user]["currentlogintimestamp"]

        if "totalloginseconds" not in data[user]:
            data[user]["totalloginseconds"] = 0

        data[user]["totalloginseconds"] += online_time.seconds

        #Clear currentlogintimestamp
        data[user].pop("currentlogintimestamp")

        #Set logout time
        data[user]["lastlogout"] = stop_time
    return None


def add_user_killed_by(user, killed_by):
    if "killedby" not in data[user]:
        data[user]["killedby"] = {}

    if killed_by not in data[user]["killedby"]:
        data[user]["killedby"][killed_by] = 0

    data[user]["killedby"][killed_by] += 1
    return None


def add_user_accidental_death(user, cause):
    if "suicides" not in data[user]:
        data[user]["suicides"] = {}

    if cause not in data[user]["suicides"]:
        data[user]["suicides"][cause] = 0

    data[user]["suicides"][cause] += 1
    return None

def add_user_assisted_death(user, cause):
    if "assisted_suicides" not in data[user]:
        data[user]["assisted_suicides"] = {}

    if cause not in data[user]["assisted_suicides"]:
        data[user]["assisted_suicides"][cause] = 0

    data[user]["assisted_suicides"][cause] += 1
    return None


def handle_login(regexresult):
    time = parse_time(regexresult)
    user = regexresult[7]

    handle_user(user)

    data[user]["currentlogintimestamp"] = time
    data[user]["lastlogin"] = time

    if "firstlogin" not in data[user]:
        data[user]["firstlogin"] = time

    return None


def handle_logout(regexresult):
    time = parse_time(regexresult)
    user = regexresult[7]

    handle_user(user)
    add_user_time(user, time)
    return None


def handle_server_restart(regexresults):
    time = parse_time(regexresults)

    #Calculate logged in times for all users with currentlogintimestamp entry, then clear the currentlogintimestamps
    for user in data:
        add_user_time(user, time)
    return None


def handle_server_stop(regexresults):
    return handle_server_restart(regexresults)


def handle_server_start(regexresults):
    #We can call handle_server_restart in case of a server crash.
    #No duplicate time will be logged since currentlogintimestamp is cleared.
    return handle_server_restart(regexresults)


def handle_server_name(regexresults):
    global server_name

    server_name = regexresults[7]

    return None


def handle_slain(regexresults):
    time = parse_time(regexresults)
    user = regexresults[7]
    killed_by = regexresults[8]

    handle_user(user)

    add_user_killed_by(user, killed_by)
    return None


def handle_blown_up(regexresults):
    return handle_slain(regexresults)


def handle_shot(regexresults):
    return handle_slain(regexresults)


def handle_fell(regexresults):
    user = regexresults[7]
    cause = "fallen to death"

    add_user_accidental_death(user, cause)
    return None

def handle_pricked(regexresults):
    user = regexresults[7]
    cause = "pricked to death"

    add_user_accidental_death(user, cause)
    return None

def handle_lava(regexresults):
    user = regexresults[7]
    cause = "swum in lava"

    add_user_accidental_death(user, cause)
    return None


def handle_inflames(regexresults):
    user = regexresults[7]
    cause = "burnt to death"

    add_user_accidental_death(user, cause)
    return None


def handle_drowned(regexresults):
    user = regexresults[7]
    cause = "drowned"

    add_user_accidental_death(user, cause)
    return None

def handle_suffocated(regexresults):
    user = regexresults[7]
    cause = "suffocated in a wall"

    add_user_accidental_death(user, cause)
    return None

def handle_fell_by(regexresults):
    user = regexresults[7]
    villain = regexresults[8]
    cause = "fell to death fighting " + villain

    add_user_assisted_death(user, cause)
    return None

def handle_burnt_by(regexresults):
    user = regexresults[7]
    villain = regexresults[8]
    cause = "burnt to death fighting " + villain

    add_user_assisted_death(user, cause)
    return None

def handle_chat_message(regexresults):
    time = parse_time(regexresults)
    user = regexresults[7]
    message = regexresults[8]
    return mc_dynchat.parse_chat_message(time, user, message, data)


def handle_web_chat_message(regexresults):
    return handle_chat_message(regexresults)
