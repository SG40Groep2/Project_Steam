import json
import requests
import io
from urllib.request import urlopen
from PIL import Image, ImageTk

import pprint

# import time
# import RPi.GPIO as GPIO
#
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(0)
#
# clock_pin = 19
# data_pin = 26
# switch1 = 23
# sr04_trig = 21
# sr04_echo = 20
# servo = 25
# pieper = 24
# shift_clock_pin = 5
# latch_clock_pin = 6
# data_pin_hc595 = 13
#
# GPIO.setup(clock_pin, GPIO.OUT)
# GPIO.setup(data_pin, GPIO.OUT)
# GPIO.setup( switch1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
# GPIO.setup(sr04_trig, GPIO.OUT)
# GPIO.setup(sr04_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(servo, GPIO.OUT)
# GPIO.setup(pieper, GPIO.OUT)
# GPIO.setup( shift_clock_pin, GPIO.OUT )
# GPIO.setup( latch_clock_pin, GPIO.OUT )
# GPIO.setup( data_pin_hc595, GPIO.OUT )

ahmed_id = 76561198298331661
key = '66D8DC4C544F361B28D4D5491FE8F07A'
ruben_id = 76561198841435984


class Data:
    @staticmethod
    def get_json():
        with open("steam.json", "r") as steam:
            return json.load(steam)

    @staticmethod
    def owned_games(key, id):
        owned_games = requests.get(
            f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}&include_appinfo=TRUE&format=json')
        json = owned_games.json()
        return json

    @staticmethod
    def get_friends(key, id):
        friend_list = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={id}&relationship=friend')
        json = friend_list.json()
        return json

    @staticmethod
    def get_bans():
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        ahmed_id = 76561198298331661
        ruben_id = 76561198841435984
        bans = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1?key={key}&steamids={ahmed_id}')
        json = bans.json()
        return json

    @staticmethod
    def get_profile_info(key, id):
        profile = requests.get(
            f' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={id}&format=json')
        json = profile.json()
        return json

    @staticmethod
    def get_news_app(appid):
        news = requests.get(
            f'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}count=3&maxlength=300&format=json')
        json = news.json()
        return json

    @staticmethod
    def get_game_info(appid):
        profile = requests.get(
            f'http://store.steampowered.com/api/appdetails/?appids=${appid}&include_appinfo ')

        return profile.json()

    @staticmethod
    def get_player_achievemenets(appid):
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        ahmed_id = 76561198298331661
        achievements = requests.get(
            f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={key}&steamid={ahmed_id}")
        json = achievements.json()
        return json

    @staticmethod
    def get_global_achievements(gameid):
        achievements = requests.get(
            f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={gameid}&format=json")
        json = achievements.json()
        return json

    @staticmethod
    def verwerk_online_info():
        eindresultaat_offline = []
        eindresultaat_online = []
        lijst_get_friends = Data.get_friends(key, ahmed_id)
        aantal_vrienden = len(lijst_get_friends['friendslist']['friends'])  # De hoeveelheid vrienden
        vrienden_ids = lijst_get_friends['friendslist']['friends']
        # print(f'Aantal vrienden           :    {aantal_vrienden}')
        lijst_vriend_ids = []
        for x in range(aantal_vrienden):
            lijst_vriend_ids.append(vrienden_ids[x]['steamid'])
        # print(f'Lijst met ids van vrienden:    {lijst_vriend_ids}')
        loper = 0
        for x in range(aantal_vrienden):  # elke vriend langsgaan
            lijst_get_online_info = Data.get_online_info(lijst_vriend_ids[loper])
            id = lijst_get_online_info["response"]["players"][0]["steamid"]
            nummer = lijst_get_online_info["response"]["players"][0]["personastate"]
            gamernaam = lijst_get_online_info["response"]["players"][0]["personaname"]
            # print(f'Informatie laden van      :    {gamernaam}')
            foto = Data.get_online_info(lijst_vriend_ids[loper])["response"]["players"][0]["avatarfull"]
            if nummer == 0 or nummer == 2 or nummer == 3 or nummer == 4:  # als de vriend offline is, dan geeft ie deze variabelen mee.
                keuze = f'Offline'
                eindresultaat_offline += [id, gamernaam, keuze, foto]
            elif nummer == 1 or nummer == 6 or nummer == 7:  # als de vriend online is, dan geeft ie deze variabelen mee.
                keuze = f'Online'
                eindresultaat_online += [id, gamernaam, keuze, foto]
            loper += 1

        aantal_online = len(eindresultaat_online) // 4
        aantal_offline = len(eindresultaat_offline) // 4
        print_online = []
        if aantal_online > 0:
            for x in range(aantal_online):
                print_online.append(eindresultaat_online[x * 4 + 1])
        print_offline = []
        if aantal_offline > 0:
            for x in range(aantal_offline):
                print_offline.append(eindresultaat_offline[x * 4 + 1])
        # print(f'Aantal mens(en) online    :    {aantal_online}, {print_online}')
        # print(f'Aantal mens(en) offline   :    {aantal_offline}, {print_offline}')

        almost = Data.offline_online(aantal_vrienden, aantal_online, eindresultaat_online,
                                     eindresultaat_offline)  # functie aanroepen voor welke gegevens er gepakt moeten worden
        if aantal_vrienden == 2:
            foto1 = Data.verwerk_foto(almost[0][3])  # De foto door de functie halen zodat de foto werkt
            almost[0][3] = foto1  # De foto vervangen
            foto2 = Data.verwerk_foto(almost[1][3])
            almost[1][3] = foto2
        elif aantal_vrienden == 1:
            foto1 = Data.verwerk_foto(almost[0][3])
            almost[0][3] = foto1
        elif aantal_vrienden == 3:
            foto1 = Data.verwerk_foto(almost[0][3])
            almost[0][3] = foto1
            foto2 = Data.verwerk_foto(almost[1][3])
            almost[1][3] = foto2
            foto3 = Data.verwerk_foto(almost[2][3])
            almost[2][3] = foto3
        return almost

    @staticmethod
    def offline_online(aantal_vrienden, aantal_online, eindresultaat_online, eindresultaat_offline):
        if aantal_vrienden >= 3:
            if aantal_online == 3:
                totaallijst = [[], [], []]
                totaallijst[0] = [eindresultaat_online[0], eindresultaat_online[1],
                                  eindresultaat_online[2], eindresultaat_online[3]]
                totaallijst[1] = [eindresultaat_online[4], eindresultaat_online[5],
                                  eindresultaat_online[6], eindresultaat_online[7]]
                totaallijst[2] = [eindresultaat_online[8], eindresultaat_online[9],
                                  eindresultaat_online[10], eindresultaat_online[11]]
                return totaallijst
            elif aantal_online == 2:
                totaallijst = [[], [], []]
                totaallijst[0] = [eindresultaat_online[0], eindresultaat_online[1],
                                  eindresultaat_online[2], eindresultaat_online[3]]
                totaallijst[1] = [eindresultaat_online[4], eindresultaat_online[5],
                                  eindresultaat_online[6], eindresultaat_online[7]]
                totaallijst[2] = [eindresultaat_offline[0], eindresultaat_offline[1],
                                  eindresultaat_offline[2], eindresultaat_offline[3]]  # gegevens toevoegen
                return totaallijst
            elif aantal_online == 1:
                totaallijst = [[], [], []]
                totaallijst[0] = [eindresultaat_online[0], eindresultaat_online[1],
                                  eindresultaat_online[2], eindresultaat_online[3]]
                totaallijst[1] = [eindresultaat_offline[0], eindresultaat_offline[1],
                                  eindresultaat_offline[2], eindresultaat_offline[3]]
                totaallijst[2] = [eindresultaat_offline[4], eindresultaat_offline[5],
                                  eindresultaat_offline[6], eindresultaat_offline[7]]
                return totaallijst
            elif aantal_online == 0:
                totaallijst = [[], [], []]
                totaallijst[0] = [eindresultaat_offline[0], eindresultaat_offline[1],
                                  eindresultaat_offline[2], eindresultaat_offline[3]]
                totaallijst[1] = [eindresultaat_offline[4], eindresultaat_offline[5],
                                  eindresultaat_offline[6], eindresultaat_offline[7]]
                totaallijst[2] = [eindresultaat_offline[8], eindresultaat_offline[9],
                                  eindresultaat_offline[10], eindresultaat_offline[11]]
                return totaallijst
        else:
            if aantal_vrienden == 1:
                if aantal_online == aantal_vrienden:
                    return eindresultaat_online  # gegevens van deze ene online vriend
                else:
                    return eindresultaat_offline  # gegevens van deze ene offline vriend
            elif aantal_vrienden == 2:
                if aantal_online == aantal_vrienden:
                    totaallijst = [[], []]
                    totaallijst[0] = [eindresultaat_online[0], eindresultaat_online[1],
                                      eindresultaat_online[2], eindresultaat_online[3]]
                    totaallijst[1] = [eindresultaat_online[4], eindresultaat_online[5],
                                      eindresultaat_online[6], eindresultaat_online[7]]
                    return totaallijst  # gegevens van deze 2 online vrienden
                elif aantal_online == 0:
                    totaallijst = [[], []]
                    totaallijst[0] = [eindresultaat_offline[0], eindresultaat_offline[1],
                                      eindresultaat_offline[2], eindresultaat_offline[3]]
                    totaallijst[1] = [eindresultaat_offline[4], eindresultaat_offline[5],
                                      eindresultaat_offline[6], eindresultaat_offline[7]]
                    return totaallijst  # gegevens van deze 2 offline vrienden
                else:
                    totaallijst = [eindresultaat_online, eindresultaat_offline]
                    return totaallijst  # gegevens van deze 2 vrienden, 1 off 1 on

    @staticmethod
    def verwerk_foto(foto):
        image_bytes = urlopen(foto).read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image

    @staticmethod
    def gameid_of_mostplayed_game():
        lijst = Data.owned_games(key, ahmed_id)  # De gehele lijst die hij ophaald van de steam api
        aantal_games = lijst['response']['game_count']  # aantal games
        hoogste_play_time = lijst['response']['games'][0]['playtime_forever']
        appid_hoogste = lijst['response']['games'][0]['appid']
        for x in range(aantal_games):
            playtime = lijst['response']['games'][x]['playtime_forever']
            if playtime > hoogste_play_time:
                hoogste_play_time = playtime
                appid_hoogste = lijst['response']['games'][x]['appid']
        return appid_hoogste

    @staticmethod
    def get_online_info(id):
        ahmed_id = 76561198298331661
        ruben_id = 76561198841435984
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        profile = requests.get(
            f' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={id}&format=json')
        json = profile.json()
        return json

    @staticmethod
    def procent_uitgespeeld():
        list = Data.get_player_achievemenets(Data.gameid_of_mostplayed_game())
        aantal_achievements = len(list['playerstats']['achievements'])
        aantal_achievements_gehaald = 0
        for x in range(aantal_achievements):
            if list['playerstats']['achievements'][x]['achieved'] >= 1:
                aantal_achievements_gehaald += list['playerstats']['achievements'][x]['achieved']
        aantal_procent = aantal_achievements_gehaald / aantal_achievements * 100
        return aantal_procent

    @staticmethod
    def gemiddeld_procent():
        while True:
            lijst = Data.get_global_achievements(Data.gameid_of_mostplayed_game())['achievementpercentages'][
                'achievements']
            totaal_procent = 0
            for x in lijst:
                totaal_procent += x['percent']
            gemiddeld_procent = totaal_procent / len(lijst)
            eigen_procent = Data.procent_uitgespeeld()
            Data.normal_walk(gemiddeld_procent, eigen_procent)





class Algo:
    @staticmethod
    def my_insertion_sort(steam, key, reverse):
        """ Sorteer steamdata op prijs
         Hieronder staat de pseudocode van een sorteeralgoritme:
    1. Startend vanaf het begin van een lijst,
    vergelijk elk element met zijn volgende buur.
    2. Als het element groter is dan zijn volgende buur,
    verwissel ze van plaats.
    3. Doorloop zo de lijst tot het eind.
    4. Als er verwisselingen zijn geweest bij stap 2., ga naar stap 1"""
        sorted_json = []
        # Copy steam data to a list of dictionaries
        for game in steam:
            sorted_json.append(game)

        i = 0
        while i != len(sorted_json):  # 3
            for number in range(0, len(sorted_json) - 1):  # 1
                iets = sorted_json[number][key]
                nogiets = sorted_json[number + 1][key]
                if iets >= nogiets:  # 2
                    sorted_json[number], sorted_json[number + 1] = \
                        sorted_json[number + 1], sorted_json[number]  # 2
                    number -= i  # `4
            i += 1
        if reverse:
            return sorted_json[::-1]
        return sorted_json

    @staticmethod
    def linear_search(lst, target, key):
        for i in range(len(lst) - 1):
            if target == lst[i][key]:
                return True
        return False





    # merge sort algoritme
    # @staticmethod
    # def merge_sort(array, left_index, right_index, optie):
    #     if left_index >= right_index:
    #         return array
    #
    #     middle = (left_index + right_index) // 2
    #     Data.merge_sort(array, left_index, middle, optie)
    #     Data.merge_sort(array, middle + 1, right_index, optie)
    #     Data.merge(array, left_index, right_index, middle, optie)
    #
    # @staticmethod
    # def merge(array, left_index, right_index, middle, optie):
    #     left_copy = array[left_index: middle + 1]
    #     right_copy = array[middle + 1: right_index + 1]
    #     left_copy_index = 0
    #     right_copy_index = 0
    #     sorted_index = left_index
    #     while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
    #         if left_copy[left_copy_index][optie] <= right_copy[right_copy_index][optie]:
    #             array[sorted_index] = left_copy[left_copy_index]
    #             left_copy_index += 1
    #         else:
    #             array[sorted_index] = right_copy[right_copy_index]
    #             right_copy_index += 1
    #         sorted_index += 1
    #     while left_copy_index < len(left_copy):
    #         array[sorted_index] = left_copy[left_copy_index]
    #         left_copy_index += 1
    #         sorted_index += 1
    #
    #     while right_copy_index < len(right_copy):
    #         array[sorted_index] = right_copy[right_copy_index]
    #         right_copy_index += 1
    #         sorted_index += 1
    #
    # @staticmethod
    # def sort_list(lijst, optie):
    #     Data.merge_sort(lijst, 0, len(lijst) - 1, optie)
    #     return lijst
    #
    # @staticmethod
    # def sort_a_z():
    #     for x in range(0, len(Data.get_json())):
    #         name = Data.sort_list(Data.get_json(), 'name')
    #         return (name[x]['name'])
    #
    # @staticmethod
    # def sort_z_a():
    #     for x in range(len(Data.get_json())-1, 0, -1):
    #         name = Data.sort_list(Data.get_json(), 'name')
    #         return name[x]['name']


aanbevolen_game = 'The Witcher'

f = Data.owned_games(key, ahmed_id)
lst = []
for i in range(0, 10):
    dict = {}
    dict['name'] = f['response']['games'][i]['name']
    dict['hours_played'] = round(f['response']['games'][i]['playtime_forever'] / 60)
    dict['icon'] = f['response']['games'][i]['img_icon_url']
    dict['logo'] = f['response']['games'][i]['img_logo_url']
    lst.append(dict)
    # owned = f['response']['games'][i]['name'], round(f['response']['games'][i]['playtime_forever'] / 60), 'uur gespeeld'


# pprint.pprint(lst)


class Ti:
    # @staticmethod
    # def hc595(shift_clock_pin, latch_clock_pin, data_pin, value, delay):
    #     for y in range(8):
    #         if value % 2 == 1:
    #             GPIO.output(shift_clock_pin, 1)
    #             GPIO.output(latch_clock_pin, 1)
    #             GPIO.output(latch_clock_pin, 0)
    #             GPIO.output(shift_clock_pin, 0)
    #             GPIO.output(data_pin, 1)
    #         else:
    #             GPIO.output(data_pin, 0)
    #
    #         value = value // 2
    #     time.sleep(delay)
    #
    # @staticmethod
    # def normal_walk(gemiddeld_procent, eigen_procent):
    #     global shift_clock_pin, latch_clock_pin, data_pin
    #     if eigen_procent >= gemiddeld_procent:
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 1, 0.2)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 2, 0.2)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 4, 0.2)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 8, 0.2)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 16, 0.2)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 32, 0.2)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 64, 0.2)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 128, 0.2)
    #     else:
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 1,  1)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 2,  1)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 4,  1)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 8,  1)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 16, 1)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 32, 1)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 64, 1)
    #         Data.hc595(shift_clock_pin, latch_clock_pin, data_pin_hc595, 128,1)

    pass

# def leuke_dingen_uitprinten():
#     lijst_owned_games = Data.get_owned_games()
#     aantal_games = lijst_owned_games['response']['game_count']
#     appid_hoogste = lijst_owned_games['response']['games'][0]['appid']
#     hoogste_play_time = lijst_owned_games['response']['games'][0]['playtime_forever']
#     for x in range(aantal_games):
#         playtime = lijst_owned_games['response']['games'][x]['playtime_forever']
#         if playtime > hoogste_play_time:
#             hoogste_play_time = playtime
#             appid_hoogste = lijst_owned_games['response']['games'][x]['appid']
#     lijst_player_achievements = Data.get_player_achievemenets(appid_hoogste)
#     aantal_achievements = len(lijst_player_achievements['playerstats']['achievements'])
#     aantal_achievements_gehaald = 0
#     for x in range(aantal_achievements):
#         if lijst_player_achievements['playerstats']['achievements'][x]['achieved'] >= 1:
#             aantal_achievements_gehaald += lijst_player_achievements['playerstats']['achievements'][x]['achieved']
#     aantal_procent = round(aantal_achievements_gehaald / aantal_achievements * 100, 2)
#     print(f"Aantal bans               :    {Data.get_bans()['players'][0]['NumberOfVACBans']}")
#     print(f"Aantal games              :    {lijst_owned_games['response']['game_count']}")
#     print(f"Meest gespeelde game      :    {Data.get_player_achievemenets(appid_hoogste)['playerstats']['gameName']}")
#     print(f"Totaal aantal achievements:    {aantal_achievements}")
#     print(f"gehaalde achievements     :    {aantal_achievements_gehaald}")
#     print(f"% gehaald van je game     :    {aantal_procent}%")


# pprint.pprint(Data.get_friends(key, ahmed_id))
# pprint.pprint((Data.get_profile_info(key,ruben_id )))
# pprint.pprint(Data.owned_games(key, ahmed_id))
# pprint.pprint(Data.get_news_app(20900))

