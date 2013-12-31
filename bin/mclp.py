#!/usr/bin/env python
import re, datetime, operator, sys
import mc_actions
import mc_datahandler


def print_help():
    print("Minecraft Log Parser usage:")
    print("  mclp [path to server.log]")


def read_log(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    return lines


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
    lines = read_log(logfile_path)
    for line in lines:
        [action, regexresult] = find_action_match(line)
        if action is not None:
            execute_action(action, regexresult)


if len(sys.argv) != 2:
    print_help()
    sys.exit(0)
elif sys.argv[1]:
    filepath = sys.argv[1]

main(filepath)


mc_datahandler.run(mc_actions.server_name, mc_actions.data)