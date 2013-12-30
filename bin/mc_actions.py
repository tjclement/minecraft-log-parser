import re

DATETIME = "([0-9]{4})\-([0-9]{2})\-([0-9]{2}) ([0-2][0-9])\:([0-9]{2})\:([0-9]{2}) ";

actions = {
    "login": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) ?\[\/[0-9.]{4,15}\:[0-9]*\]"),
    "logout": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) lost connection"),
    "server_stop": re.compile(DATETIME + "\[INFO\] Stopping server"),
    "blown_up": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was blown up by (.?)*"),
    "shot": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was shot by (.?)*"),
    "slain": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was slain by (.?)*"),
    "burnt_by": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was burnt to a crisp whilst fighting (.?)*"),
    "lava": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) tried to swim in lava"),
    "inflames": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) went up in flames"),
    "fell": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) fell from a high place"),
    "fell_by": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) was doomed to fall by (.?)*"),
    "drowned": re.compile(DATETIME + "\[INFO\] ([A-z0-9]*) drowned"),
    "server_start": re.compile(DATETIME + "\[INFO\] Starting minecraft server")
}

data = []


def handle_login(regexresult):
    print "Executing handle_login"
    return None