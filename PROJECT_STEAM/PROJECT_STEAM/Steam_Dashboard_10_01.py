# from merge_sort import *
import json
import requests
import io
from urllib.request import urlopen
from PIL import Image, ImageTk
import time


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

class Data:
    @staticmethod
    def get_json():
        with open("steam.json", "r") as steam:
            return json.load(steam)

    @staticmethod
    def sort_json(json):
        return sorted(json, key=lambda x: x['name'])

    @staticmethod
    def get_friends():
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        ahmed_id = 76561198298331661
        ruben_id = 76561198841435984
        friend_list = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={ahmed_id}&relationship=friend')
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
    def get_owned_games():
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        ahmed_id = 76561198298331661
        games = requests.get(
            f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={ahmed_id}&format=json")
        json = games.json()
        return json

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

    # Functie voor TI gedeelte, dus niet aankomen
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
    def verwerk_online_info():
        eindresultaat_offline = []
        eindresultaat_online = []
        lijst_get_friends = Data.get_friends()
        aantal_vrienden = len(lijst_get_friends['friendslist']['friends'])  # De hoeveelheid vrienden
        vrienden_ids = lijst_get_friends['friendslist']['friends']
        print(f'Aantal vrienden           :    {aantal_vrienden}')
        lijst_vriend_ids = []
        for x in range(aantal_vrienden):
            lijst_vriend_ids.append(vrienden_ids[x]['steamid'])
        print(f'Lijst met ids van vrienden:    {lijst_vriend_ids}')
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
        print(f'Aantal mens(en) online    :    {aantal_online}, {print_online}')
        print(f'Aantal mens(en) offline   :    {aantal_offline}, {print_offline}')

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

    # @staticmethod
    # def apa102_send_bytes(clock_pin, data_pin, bytes):
    #     for byte in bytes:
    #         for bit in byte:
    #             if bit == '1':
    #                 GPIO.output(data_pin, 1)
    #             else:
    #                 GPIO.output(data_pin, 0)
    #             GPIO.output(clock_pin, 1)
    #             GPIO.output(clock_pin, 0)
    #
    #
    # @staticmethod
    # def apa102(clock_pin, data_pin, colors):
    #     nullen_bytes = [[], [], [], []]
    #     for x in range(4):
    #         for i in range(8):
    #             nullen_bytes.append(str(0))
    #     Data.apa102_send_bytes(clock_pin, data_pin, nullen_bytes)
    #
    #     ledjes = [[], [], [], []]
    #     for x in range(8):
    #         ledjes[0] = str(format(195, '08b'))
    #         for i in range(3):
    #             ledjes[i + 1] = str(format(colors[x][i], '08b'))
    #         Data.apa102_send_bytes(clock_pin, data_pin, ledjes)
    #
    #     een_bytes = [[], [], [], []]
    #     for x in range(4):
    #         for i in range(8):
    #             een_bytes.append(str(1))
    #     Data.apa102_send_bytes(clock_pin, data_pin, een_bytes)
    #
    # @staticmethod
    # def gedachte_neopixels():
    #     while True:
    #         lijst_get_friends = Data.get_friends()
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
    #         Data.neopixels(aantal_online)
    #         time.sleep(0.5)
    #
    # @staticmethod
    # def neopixels(aantal):
    #     red = [0, 0, 255]
    #     green = [0, 255, 0]
    #     knipperen = [[], [], [], [], [], [], [], []]
    #     for x in range(aantal):
    #         knipperen[7-x] = green
    #     for x in range(8 - aantal):
    #         knipperen[x] = red
    #
    #     Data.apa102(clock_pin, data_pin, knipperen)
    #     time.sleep(1.5)
    #
    # @staticmethod
    # def sr04(trig_pin, echo_pin, pieper):
    #     while True:
    #         GPIO.output(trig_pin, True)
    #         time.sleep(0.000001)
    #         GPIO.output(trig_pin, False)
    #
    #         begintijd = time.time()
    #         stoptijd = time.time()
    #
    #         while GPIO.input(echo_pin) == 0:
    #             begintijd = time.time()
    #         while GPIO.input(echo_pin) == 1:
    #             stoptijd = time.time()
    #
    #         totale_tijd = stoptijd - begintijd
    #         afstand = totale_tijd // 0.000058
    #
    #         Data.servo_pulse(servo,afstand)
    #         Data.pieper_functie(pieper, afstand)
    #         time.sleep(0.5)
    #
    # @staticmethod
    # def servo_pulse(pin_nr, afstand):
    #     afstand = afstand - 20
    #     var = afstand/ 10
    #     var = var + 2
    #     if var >= 100:
    #         var = 99.999999
    #     pwm_servo = GPIO.PWM(pin_nr, 50)
    #     pwm_servo.start(var)
    #     time.sleep(0.02)
    #
    # @staticmethod
    # def pieper_functie(pieper,afstand):
    #     if afstand < 20:
    #         print(f'Pieper gaat af!!')
    #         GPIO.output(pieper, 0)
    #     else:
    #         GPIO.output(pieper, 1)

    @staticmethod
    def gameid_of_mostplayed_game():
        lijst = Data.get_owned_games()  # De gehele lijst die hij ophaald van de steam api
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


def leuke_dingen_uitprinten():
    lijst_owned_games = Data.get_owned_games()
    aantal_games = lijst_owned_games['response']['game_count']
    appid_hoogste = lijst_owned_games['response']['games'][0]['appid']
    hoogste_play_time = lijst_owned_games['response']['games'][0]['playtime_forever']
    for x in range(aantal_games):
        playtime = lijst_owned_games['response']['games'][x]['playtime_forever']
        if playtime > hoogste_play_time:
            hoogste_play_time = playtime
            appid_hoogste = lijst_owned_games['response']['games'][x]['appid']
    lijst_player_achievements = Data.get_player_achievemenets(appid_hoogste)
    aantal_achievements = len(lijst_player_achievements['playerstats']['achievements'])
    aantal_achievements_gehaald = 0
    for x in range(aantal_achievements):
        if lijst_player_achievements['playerstats']['achievements'][x]['achieved'] >= 1:
            aantal_achievements_gehaald += lijst_player_achievements['playerstats']['achievements'][x]['achieved']
    aantal_procent = round(aantal_achievements_gehaald / aantal_achievements * 100, 2)
    print(f"Aantal bans               :    {Data.get_bans()['players'][0]['NumberOfVACBans']}")
    print(f"Aantal games              :    {lijst_owned_games['response']['game_count']}")
    print(f"Meest gespeelde game      :    {Data.get_player_achievemenets(appid_hoogste)['playerstats']['gameName']}")
    print(f"Totaal aantal achievements:    {aantal_achievements}")
    print(f"gehaalde achievements     :    {aantal_achievements_gehaald}")
    print(f"% gehaald van je game     :    {aantal_procent}%")
