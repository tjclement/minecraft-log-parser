import requests
import time
import createpage

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24
MONTH = DAY * 30


def seconds_to_formatted_string(time_seconds):
    if time_seconds <= 0:
        return "0 seconds"

    remainder = time_seconds
    output = ""

    months = int(remainder / MONTH)
    remainder %= MONTH

    days = int(remainder / DAY)
    remainder %= DAY

    hours = int(remainder / HOUR)
    remainder %= HOUR

    minutes = int(remainder / MINUTE)
    remainder %= MINUTE

    seconds = remainder

    if months > 0:
        output += "%d months, " % months
    if days > 0:
        output += "%d days, " % days
    if hours > 0:
        output += "%d hours, " % hours
    if minutes > 0:
        output += "%d minutes, " % minutes

    if time_seconds > MINUTE:
        output += "and "

    output += "%d seconds" % seconds
    return output


def run(server_name, user_data):
    for user in user_data:
        if "totalloginseconds" in user_data[user]:
            total_time = user_data[user]["totalloginseconds"]

            user_data[user]["totalloginformatted"] = seconds_to_formatted_string(total_time)

        #print user, ":", user_data[user]
    createpage.createpage(server_name, user_data)
    return None
