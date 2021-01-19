import requests


ahmed_id = 76561198298331661
key = '66D8DC4C544F361B28D4D5491FE8F07A'
ruben_id = 76561198841435984


class Api:
    """ Alle functies in class Api zijn een wrapper voor de steamwebapi.
     https://developer.valvesoftware.com/wiki/Steam_Web_API#License_and_further_documentation"""

    def __init__(self, key):
        self.key = key

    def get_friends(self, id):
        friend_list = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.key}&steamid={id}&relationship=friend')
        json = friend_list.json()
        return json

    def get_profile_info(self, id):
        profile = requests.get(
            f' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.key}&steamids={id}&format=json')
        json = profile.json()
        return json

    def get_news_app(self, appid):
        news = requests.get(
            f'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}count=3&maxlength=300&format=json')
        json = news.json()
        return json

    def get_bans(self, id):
        bans = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1?key={self.key}&steamids={id}')
        json = bans.json()
        return json

    def owned_games(self, id):
        owned_games = requests.get(
            f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.key}&steamid={id}&include_appinfo=TRUE&format=json')
        json = owned_games.json()
        return json

    def get_game_info(self, appid):
        profile = requests.get(
            f'http://store.steampowered.com/api/appdetails/?appids={appid}&include_appinfo=TRUE&format=json ')
        return profile.json()

    def get_player_achievemenets(self, id, appid):
        # key = '66D8DC4C544F361B28D4D5491FE8F07A'
        # ahmed_id = 76561198298331661
        achievements = requests.get(
            f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={self.key}&steamid={id}")
        json = achievements.json()
        return json


app = Api(key)


class Search:
    def __init__(self, lst):
        self.lst = lst

    def binary_search(self, target, key):
        """
        Zoek een element target in gegeven lijst door middel van  binair zoeken.
        De inhoud van de gegeven lijst verandert niet.

        1. Zet mini = 0 en maxi = lengte van lst-1
        2. Zet index op het gemiddelde van mini en maxi
        3. Als element e op positie index van lijst lst gelijk is aan
        target, retourneer TRUE + index – target is gevonden!
        4. Als element e op positie index van lijst lst kleiner is dan
        target, dan zet mini = index + 1
        5. Als element e op positie index van lijst lst groter is dan
        target, dan zet maxi = index – 1
        6. Ga naar stap 2.

        """

        lst = sorted(self.lst, key=lambda x: x[key])  # gesoorteerde lijst
        min = 0  # 1
        max = len(self.lst) - 1  # 1

        while max >= min:  # 6
            guess = (min + max) // 2  # 2

            if lst[guess][key] == target:  # 3
                return True, guess  # 3

            elif max < min:
                return False

            elif lst[guess][key] < target:  # 4
                min = guess + 1

            elif lst[guess][key] > target:  # 5
                max = guess - 1
        return False  # target zit niet in de lijst
