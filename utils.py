import json


def open_automaton(path):
    with open(path) as json_file:
        automaton = json.load(json_file)

    return automaton
