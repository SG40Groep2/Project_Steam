import json
import pprint


class Data:
    pass


class Game:
    pass


class Statistics:
    pass


def get_json():
    with open("steam.json", "r") as steam:
        return json.load(steam)

def sort_json(json):
    return sorted(json, key=lambda i: i['name'])

def get_games(json):
    return sort_json(json)[0]['name']

#pprint.pprint(get_json())

pprint.pprint(sort_json(get_json()))
# print(get_games(get_json()))
# print(type(get_json()))
eerste_game = get_games(get_json())