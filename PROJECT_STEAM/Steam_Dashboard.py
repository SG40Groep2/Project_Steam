import json
import requests


class Data:
    @staticmethod
    def get_json():
        with open("steam.json", "r") as steam:
            return json.load(steam)
    @staticmethod
    def sort_json(json):
        return sorted(json, key=lambda i: i['name'])

    @staticmethod
    def owned_games():
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        owned_games = requests.get(
            f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid=76561198298331661&format=json')
        json = owned_games.json()
        return json

    @staticmethod
    def get_friends():
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        friend_list = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid=76561198298331661&relationship=friend')
        json = friend_list.json()
        return json

    @staticmethod
    def get_profile_info():
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        profile = requests.get(
            f' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids=76561198298331661&format=json')
        json = profile.json()
        return json

    @staticmethod
    def get_news_app(appid):
        news = requests.get(
            f'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}count=3&maxlength=300&format=json')
        json = news.json()
        return Data.sort_json(json)


aanbevolen_game = Data.sort_json(Data.get_json())[0]['name']

