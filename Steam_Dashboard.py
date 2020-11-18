import json

def get_json():
    with open("steam.json", "r") as steam:
        return json.load(steam)

def sort_json(json):
    pass

def get_games(json):
    return json[0]["name"]

print(type(get_json()))

eerste_game = get_games(get_json())