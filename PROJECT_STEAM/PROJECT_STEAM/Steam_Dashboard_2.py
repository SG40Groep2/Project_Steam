import json
import requests
import io
from urllib.request import urlopen
from PIL import Image, ImageTk
import time
# import RPi.GPIO as GPIO
#
# ahmed_id = 76561198298331661
#
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(0)
#
# clock_pin = 19
# data_pin = 26
# switch1 = 23
#
# GPIO.setup(clock_pin, GPIO.OUT)
# GPIO.setup(data_pin, GPIO.OUT)
# GPIO.setup( switch1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

ahmed_id = 76561198298331661
class Data:
    @staticmethod
    def get_json():
        with open("steam.json", "r") as steam:
            return json.load(steam)

    @staticmethod
    def sort_json(json):
        return sorted(json, key=lambda i: i['name'])

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
        return Data.sort_json(json)

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
    def joo(lijst, id):
        loper = 0
        while True:
            if lijst[loper] == id:
                return loper
            else:
                loper+= 1
    #  nodig = hoeveelste plek staat de id van lijst in de get_online_info


    @staticmethod
    def verwerk_online_info():
        eindresultaat_offline = []
        eindresultaat_online = []
        aantal_vrienden = len(Data.get_friends()['friendslist']['friends'])  # De hoeveelheid vrienden
        vrienden_ids = Data.get_friends()['friendslist']['friends']
        #print(Data.get_friends())
        #print(f'aantal vrienden        :    {aantal_vrienden}')
        lijst_vriend_ids = []
        for x in range(aantal_vrienden):
            lijst_vriend_ids.append(vrienden_ids[x]['steamid'])
        #print(lijst_vriend_ids)
        loper = 0
        for x in range(aantal_vrienden):  # elke vriend langsgaan
            id = Data.get_online_info(lijst_vriend_ids[loper])["response"]["players"][0]["steamid"]
            #print(id)
            # index_lijst_vriend_ids = Data.joo(lijst_vriend_ids, id)
            nummer = Data.get_online_info(lijst_vriend_ids[loper])["response"]["players"][0]["personastate"]
            gamernaam = Data.get_online_info(lijst_vriend_ids[loper])["response"]["players"][0]["personaname"]
            # print(gamernaam)
            # print(Data.get_online_info(lijst_vriend_ids[loper])["response"]["players"][0])
            foto = Data.get_online_info(lijst_vriend_ids[loper])["response"]["players"][0]["avatarfull"]
            if nummer == 0 or nummer == 2 or nummer == 3 or nummer == 4:  # als de vriend offline is, dan geeft ie deze variabelen mee.
                keuze = f'Offline'
                eindresultaat_offline += [id, gamernaam, keuze, foto]
            elif nummer == 1 or nummer == 6 or nummer == 7:  # als de vriend online is, dan geeft ie deze variabelen mee.
                keuze = f'Online'
                eindresultaat_online += [id, gamernaam, keuze, foto]
            loper += 1

        aantal_online = len(eindresultaat_online) // 3
        aantal_offline = len(eindresultaat_offline) // 3
        # print(f'aantal mens(en) offline:    {aantal_offline}\naantal mens(en) online:     {aantal_online}')
        # print(eindresultaat_online)

        almost = Data.offline_online(aantal_vrienden, aantal_online, eindresultaat_online, eindresultaat_offline)  # functie aanroepen voor welke gegevens er gepakt moeten worden
        #print(almost)
        if aantal_vrienden == 2:
            foto1 = Data.verwerk_foto(almost[0][3])  # De foto door de functie halen zodat de foto werkt
            almost[0][3] = foto1  # De foto vervangen
            foto2 = Data.verwerk_foto(almost[1][3])
            almost[1][3] = foto2
            #print('2')
        elif aantal_vrienden == 1:
            foto1 = Data.verwerk_foto(almost[3])
            almost[3] = foto1
            #print('1')
        elif aantal_vrienden == 3:
            foto1 = Data.verwerk_foto(almost[3])
            almost[3] = foto1
            foto2 = Data.verwerk_foto(almost[7])
            almost[7] = foto2
            foto3 = Data.verwerk_foto(almost[11])
            almost[11] = foto3
            #print('3')
        #print(almost)
        return almost

    @staticmethod
    def offline_online(aantal_vrienden, aantal_online, eindresultaat_online, eindresultaat_offline):
        if aantal_vrienden >= 3:
            if aantal_online == 3 or aantal_online > 3:
                totaallijst = []
                for x in range(12):
                    totaallijst.append(eindresultaat_online[x])
                return totaallijst
            elif aantal_online == 2:
                totaallijst = [eindresultaat_online]
                totaallijst += [eindresultaat_offline[0], eindresultaat_offline[1],
                                eindresultaat_offline[2], eindresultaat_offline[3]]  # gegevens toevoegen
                return totaallijst
            elif aantal_online == 1:
                totaallijst = [eindresultaat_online]
                totaallijst += [eindresultaat_offline[0], eindresultaat_offline[1],
                                eindresultaat_offline[2], eindresultaat_offline[3],
                                eindresultaat_offline[4], eindresultaat_offline[5],
                                eindresultaat_offline[6], eindresultaat_offline[7]]
                return totaallijst
            elif aantal_online == 0:
                totaallijst = []
                totaallijst += [eindresultaat_offline[0], eindresultaat_offline[1],
                                eindresultaat_offline[2], eindresultaat_offline[3],
                                eindresultaat_offline[4], eindresultaat_offline[5],
                                eindresultaat_offline[6], eindresultaat_offline[7],
                                eindresultaat_offline[8], eindresultaat_offline[9],
                                eindresultaat_offline[10], eindresultaat_offline[11]]
        else:
            if aantal_vrienden == 0:
                return 'f0, je hebt geen vrienden'
            elif aantal_vrienden == 1:
                if aantal_online == aantal_vrienden:
                    return eindresultaat_online  # gegevens van deze ene online vriend
                else:
                    return eindresultaat_offline  # gegevens van deze ene offline vriend
            elif aantal_vrienden == 2:
                if aantal_online == aantal_vrienden:
                    #print('jo')
                    return eindresultaat_online  # gegevens van deze 2 online vrienden
                elif aantal_online == 0:
                    return eindresultaat_offline  # gegevens van deze 2 offline vrienden
                else:
                    totaallijst = [eindresultaat_online, eindresultaat_offline]
                    #print(totaallijst)
                    return totaallijst  # gegevens van deze 2 vrienden, 1 off 1 on


    @staticmethod
    def verwerk_foto(foto):
        image_bytes = urlopen(foto).read()

        data_stream = io.BytesIO(image_bytes)

        pil_image = Image.open(data_stream)

        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image

    #@staticmethod
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
    #     aantal_vrienden = len(Data.get_online_info(ahmed_id)["response"]["players"])
    #     aantal_online = 0
    #     for x in range(aantal_vrienden):
    #         nummer = Data.get_online_info(ahmed_id)["response"]["players"][x]["personastate"]
    #         if nummer == 1 or nummer == 6 or nummer == 7:
    #             aantal_online += 1
    #     if aantal_online > 8:
    #         aantal_online = 8
    #     Data.neopixels(aantal_online)
    #
    # @staticmethod
    # def neopixels(aantal):
    #     red = [0, 0, 255]
    #     blue = [8, 0, 0]
    #     knipperen = [[], [], [], [], [], [], [], []]
    #     for x in range(aantal):
    #         knipperen[7-x] = red
    #     for x in range(8 - aantal):
    #         knipperen[x] = blue
    #
    #     Data.apa102(clock_pin, data_pin, knipperen)
    #     time.sleep(1.5)

aantal_vrienden = len(Data.get_online_info(ahmed_id)["response"]["players"])
# for x in range(aantal_vrienden):