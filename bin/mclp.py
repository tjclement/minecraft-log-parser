#!/usr/bin/env python
import re, datetime, operator, sys, time
import mc_actions
import mc_datahandler
import mc_dynchat

reached_log_end = False


def print_help():
    print("Minecraft Log Parser usage:")
    print("  mclp [path to server.log]")


def read_log(path, interactive = True):
    f = open(path, "r")
    if interactive:
        f.seek(0, 2)
    else:
        f.seek(0)

    while 1:
        where = f.tell()
        line = f.readline()
        if not line:
            if(interactive):
                time.sleep(1)
                f.seek(where)
            else:
                return
        else:
            yield line


def find_action_match(line):
    regex = None
    action_name = None

    actions = mc_actions.actions.copy()

    for action in actions:
        if actions[action].match(line):
            action_name = action
            regex = actions[action]
            break

    if regex is not None:
        return action_name, regex.split(line)
    else:
        return None, None


def execute_action(action, regexresult):
    method_name = "handle_" + action
    method = None

    try:
        method = getattr(mc_actions, method_name)
    except AttributeError:
        print "Method %s not implemented, but an action regex was matched for it" % method_name
        return
    method(regexresult)


def main(logfile_path):
    #Loop through existing log entries first without executing the data handler on each action
    for line in read_log(logfile_path, interactive=False):
        [action, regexresult] = find_action_match(line)
        if action is not None:
            execute_action(action, regexresult)

    #Invoke data handler once
    mc_datahandler.run(mc_actions.server_name, mc_actions.data)

    #Let the server know we're online
    mc_dynchat.send_chat_message("My system is now online.")

    #Invoke data handler interactively upon every new action
    for line in read_log(logfile_path):
        [action, regexresult] = find_action_match(line)
        if action is not None:
            execute_action(action, regexresult)
            mc_datahandler.run(mc_actions.server_name, mc_actions.data)


if len(sys.argv) != 2:
    print_help()
    sys.exit(0)
elif sys.argv[1]:
    filepath = sys.argv[1]

main(filepath)