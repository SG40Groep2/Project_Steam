"""
Alle code die gecomment is is om de hardware te laten werken voor het
TI gedeelte van het project

"""
#from Neopixels_steam import *
from Steam_dashboard_api import *
import json
import requests
import io
from urllib.request import urlopen
from PIL import Image, ImageTk
#import time
#import RPi.GPIO as GPIO


switch1 = 23

#GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class Data:
    @staticmethod
    def get_json():
        with open("steam.json", "r") as steam:
            return json.load(steam)


    @staticmethod
    def get_online_info(id):
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        profile = requests.get(
            f' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={id}&format=json')
        return profile.json()

    @staticmethod
    def verwerk_online_info():
        eindresultaat_offline = []
        eindresultaat_online = []
        lijst_get_friends = app.get_friends(ahmed_id)
        aantal_vrienden = len(lijst_get_friends['friendslist']['friends'])  # De hoeveelheid vrienden
        vrienden_ids = lijst_get_friends['friendslist']['friends']
        lijst_vriend_ids = []
        for x in range(aantal_vrienden):
            lijst_vriend_ids.append(vrienden_ids[x]['steamid'])
        loper = 0
        for x in range(aantal_vrienden):  # elke vriend langsgaan
            lijst_get_online_info = app.get_profile_info(lijst_vriend_ids[loper])
            id = lijst_get_online_info["response"]["players"][0]["steamid"]
            nummer = lijst_get_online_info["response"]["players"][0]["personastate"]
            gamernaam = lijst_get_online_info["response"]["players"][0]["personaname"]
            foto = app.get_profile_info(lijst_vriend_ids[loper])["response"]["players"][0]["avatarfull"]
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
        elif aantal_vrienden >= 3:
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

    # @staticmethod
    # def gedachte_neopixels():
    #     while True:
    #         lijst_get_friends = app.get_friends(ahmed_id)
    #         aantal_vrienden = len(lijst_get_friends['friendslist']['friends'])
    #         vrienden_ids = lijst_get_friends['friendslist']['friends']
    #         lijst_vriend_ids = []
    #         for x in range(aantal_vrienden):
    #             lijst_vriend_ids.append(vrienden_ids[x]['steamid'])
    #         aantal_online = 0
    #         loper = 0
    #         for x in range(aantal_vrienden):
    #             nummer = Data.get_online_info(lijst_vriend_ids[loper])["response"]["players"][0]["personastate"]
    #             if nummer == 1 or nummer == 6 or nummer == 7:
    #                 aantal_online += 1
    #             loper += 1
    #         if aantal_online > 8:
    #             aantal_online = 8
    #         neopixels(aantal_online)
    #         time.sleep(0.5)

    @staticmethod
    def gemiddeld_procent():
        lijst_owned_games = app.owned_games(ahmed_id)  # De gehele lijst die hij ophaald van de steam api
        aantal_games = lijst_owned_games['response']['game_count']  # aantal games
        hoogste_play_time = lijst_owned_games['response']['games'][0]['playtime_forever']
        appid_hoogste = lijst_owned_games['response']['games'][0]['appid']
        for x in range(aantal_games):
            playtime = lijst_owned_games['response']['games'][x]['playtime_forever']
            if playtime > hoogste_play_time:
                hoogste_play_time = playtime
                appid_hoogste = lijst_owned_games['response']['games'][x]['appid']

        lijst_player_achievements = app.get_player_achievemenets(ahmed_id,appid_hoogste)
        aantal_achievements = len(lijst_player_achievements['playerstats']['achievements'])
        aantal_achievements_gehaald = 0
        for x in range(aantal_achievements):
            if lijst_player_achievements['playerstats']['achievements'][x]['achieved'] >= 1:
                aantal_achievements_gehaald += lijst_player_achievements['playerstats']['achievements'][x]['achieved']
        eigen_procent = aantal_achievements_gehaald / aantal_achievements * 100

        lampjes = 0
        if 0 < eigen_procent <= 12.5:
            lampjes = 1
        elif 12.5 < eigen_procent <= 25:
            lampjes = 2
        elif 25 < eigen_procent <= 37.5:
            lampjes = 3
        elif 37.5 < eigen_procent <= 50:
            lampjes = 4
        elif 50 < eigen_procent <= 62.5:
            lampjes = 5
        elif 62.5 < eigen_procent <= 75:
            lampjes = 6
        elif 75 < eigen_procent <= 87.5:
            lampjes = 7
        elif 87.5 < eigen_procent <= 100:
            lampjes = 8
        return lampjes


class Sort:
    def __init__(self, lst):
        self.lst = lst

    def my_insertion_sort(self, key):
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
        for game in self.lst:
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
        return sorted_json