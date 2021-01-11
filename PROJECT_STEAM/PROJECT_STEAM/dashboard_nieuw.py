import json
import requests
import io
from urllib.request import urlopen
from PIL import Image, ImageTk


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

    # Functie voor TI gedeelte, dus niet aankomen
    @staticmethod
    def get_online_info():
        vriend_id = Data.get_friends()["friendslist"]["friends"][0]["steamid"]
        key = '66D8DC4C544F361B28D4D5491FE8F07A'
        profile = requests.get(
            f' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={vriend_id}&format=json')
        json = profile.json()
        return json

    # Functie voor TI gedeelte, dus niet aangekomen
    @staticmethod
    def verwerk_online_info():
        eindresultaat_offline = []
        eindresultaat_online = []
        laatst_online = []
        aantal_vrienden = len(Data.get_online_info()["response"]["players"])                                            # De hoeveelheid vrienden
        print(f'aantal vrienden online :    {len(Data.get_online_info()["response"]["players"])}')
        for x in range(aantal_vrienden):                                                                                # elke vriend langsgaan
            nummer = Data.get_online_info()["response"]["players"][x]["personastate"]
            gamernaam = Data.get_online_info()["response"]["players"][x]["personaname"]
            id = Data.get_online_info()["response"]["players"][x]["steamid"]
            foto = Data.get_online_info()["response"]["players"][x]["avatarfull"]
            lastlogof = Data.get_online_info()["response"]["players"][x]['lastlogoff']
            if nummer == 0 or nummer == 2 or nummer == 3 or nummer == 4:                                                # als de vriend offline is, dan geeft ie deze variabelen mee.
                keuze = f'Offline'
                eindresultaat_offline += [id, gamernaam, keuze, foto]
            elif nummer == 1 or nummer == 6 or nummer == 7:                                                             # als de vriend online is, dan geeft ie deze variabelen mee.
                keuze = f'Online'
                eindresultaat_online += [id, gamernaam, keuze, foto]
            laatst_online += [(id, lastlogof)]                                                                          #register voor wie er het laatst online was
        print(f'lijst id en lastlogoff:     {laatst_online}')
        laatst_online.sort(key=Data.tweedeblokje, reverse=True)                                                         #sorteren van de lijst

        aantal_online = len(eindresultaat_online) // 3
        aantal_offline = len(eindresultaat_offline) // 3
        print(f'aantal mens(en) offline:    {aantal_offline} \naantal mens(en) online:     {aantal_online}')

        almost = Data.offline_online(aantal_vrienden, aantal_online, eindresultaat_online, eindresultaat_offline,
                                     laatst_online)                                                                     #functie aanroepen voor welke gegevens er gepakt moeten worden
        if aantal_vrienden == 2:
            foto1 = Data.verwerk_foto(almost[3])                                                                        #De foto door de functie halen zodat de foto werkt
            almost[3] = foto1                                                                                           #De foto vervangen
            foto2 = Data.verwerk_foto(almost[7])
            almost[7] = foto2
        elif aantal_vrienden == 1:
            foto1 = Data.verwerk_foto(almost[3])
            almost[3] = foto1
        elif aantal_vrienden == 3:
            foto1 = Data.verwerk_foto(almost[3])
            almost[3] = foto1
            foto2 = Data.verwerk_foto(almost[7])
            almost[7] = foto2
            foto3 = Data.verwerk_foto(almost[11])
            almost[11] = foto3
        return almost

    @staticmethod
    def offline_online(aantal_vrienden, aantal_online, eindresultaat_online, eindresultaat_offline, laatst_online):
        if aantal_vrienden >= 3:
            if aantal_online == 3 or aantal_online > 3:
                totaallijst = []
                for x in range(12):
                    totaallijst.append(eindresultaat_online[x])
                return totaallijst
            elif aantal_online == 2:
                totaallijst = [eindresultaat_online]
                offline_persoon_id = laatst_online[0][0]                                                                # id van de persoon die laatst online is.
                index_id = eindresultaat_offline.index(offline_persoon_id)                                              # index van de persoons id in de lijst
                totaallijst += [eindresultaat_offline[index_id], eindresultaat_offline[index_id + 1],
                                eindresultaat_offline[index_id + 2],eindresultaat_offline[index_id + 3]]                # gegevens toevoegen
                return totaallijst
            elif aantal_online == 1:
                totaallijst = [eindresultaat_online]
                offline_persoon_id1 = laatst_online[0][0]
                index_id1 = eindresultaat_offline.index(offline_persoon_id1)
                totaallijst += [eindresultaat_offline[index_id1], eindresultaat_offline[index_id1 + 1],
                                eindresultaat_offline[index_id1 + 2], eindresultaat_offline[index_id1 + 3]]
                offline_persoon_id2 = laatst_online[1][0]
                index_id2 = eindresultaat_offline.index(offline_persoon_id2)
                totaallijst += [eindresultaat_offline[index_id2], eindresultaat_offline[index_id2 + 1],
                                eindresultaat_offline[index_id2 + 2], eindresultaat_offline[index_id2 + 3]]
                return totaallijst
            elif aantal_online == 0:
                totaallijst = []
                offline_persoon_id1 = laatst_online[0][0]
                index_id1 = eindresultaat_offline.index(offline_persoon_id1)
                totaallijst += [eindresultaat_offline[index_id1], eindresultaat_offline[index_id1 + 1],
                                eindresultaat_offline[index_id1 + 2], eindresultaat_offline[index_id1 + 3]]
                offline_persoon_id2 = laatst_online[1][0]
                index_id2 = eindresultaat_offline.index(offline_persoon_id2)
                totaallijst += [eindresultaat_offline[index_id2], eindresultaat_offline[index_id2 + 1],
                                eindresultaat_offline[index_id2 + 2], eindresultaat_offline[index_id2 + 3]]
                offline_persoon_id3 = laatst_online[2][0]
                index_id3 = eindresultaat_offline.index(offline_persoon_id3)
                totaallijst += [eindresultaat_offline[index_id3], eindresultaat_offline[index_id3 + 1],
                                eindresultaat_offline[index_id3 + 2], eindresultaat_offline[index_id3 + 3]]
        else:
            if aantal_vrienden == 0:
                return 'f0, je hebt geen vrienden'
            elif aantal_vrienden == 1:
                if aantal_online == aantal_vrienden:
                    return eindresultaat_online                                                                         # gegevens van deze ene online vriend
                else:
                    return eindresultaat_offline                                                                        # gegevens van deze ene offline vriend
            elif aantal_vrienden == 2:
                if aantal_online == aantal_vrienden:
                    return eindresultaat_online                                                                         # gegevens van deze 2 online vrienden
                elif aantal_online == 0:
                    return eindresultaat_offline                                                                        # gegevens van deze 2 offline vrienden
                else:
                    totaallijst = [eindresultaat_online, eindresultaat_offline]
                    return totaallijst                                                                                  # gegevens van deze 2 vrienden, 1 off 1 on

    @staticmethod
    def tweedeblokje(element):
        return element[1]

    @staticmethod
    def verwerk_foto(foto):
        image_bytes = urlopen(foto).read()

        data_stream = io.BytesIO(image_bytes)

        pil_image = Image.open(data_stream)

        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image
