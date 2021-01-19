from Steam_Dashboard_def import Data


def mean(lst):
    """ Retourneer het gemiddelde (float) van de lijst lst. """
    totaal = 0
    lengte = 0
    for nr in lst:
        totaal += nr
        lengte += 1

    return totaal / lengte


def rnge(lst):
    """ Retourneer het bereik (int) van de lijst lst. """
    maxi = 0
    mini = 0
    s = sorted(lst)
    l = len(s) - 1

    for nr in lst:
        if nr >= s[l]:
            maxi = nr
        elif nr <= s[0]:
            mini = nr
    return maxi - mini


def median(lst):
    """ Retourneer de mediaan (float) van de lijst lst. """
    lst_sorted = sorted(lst)

    lengte = 0
    for nr in lst:
        lengte += 1

    if lengte % 2 == 0:
        mid = lengte // 2 - 1
        mid_1 = mid + 1
        bereken = (lst_sorted[mid] + lst_sorted[mid_1]) / 2
        return bereken
    elif lengte % 2 != 0:
        med = lengte // 2
        antw = lst_sorted[med]
        return float(antw)


def q1(lst):
    """
    Retourneer het eerste kwartiel Q1 (float) van de lijst lst.
    Tip: maak gebruik van median()
    """
    lst_sorted = sorted(lst)

    lengte = 0
    for nr in lst:
        lengte += 1

    if len(lst) % 2 == 0:
        helft = median(lst)
        half_index = int(lengte // 2)

        half_lst = lst_sorted[0:half_index]

        return median(half_lst)

    elif len(lst) % 2 > 0:
        half = median(lst)

        afgerond = int(-1 * half // 1 * -1)
        half_index = lst_sorted.index(afgerond)

        half_lijst = lst_sorted[0:half_index]

        gem = median(half_lijst)
        return float(gem)


def q3(lst):
    """ Retourneer het derde kwartiel Q3 (float) van de lijst lst. """
    lst_sorted = sorted(lst)

    lengte = 0
    for nr in lst:
        lengte += 1

    if len(lst) % 2 == 0:
        helft = median(lst)
        half_index = int(lengte // 2)

        half_lst = lst_sorted[half_index:]

        return median(half_lst)

    elif len(lst) % 2 > 0:
        half = median(lst)

        afgerond = int(-1 * half // 1 * -1)
        half_index = lst_sorted.index(afgerond) + 1

        half_lijst = lst_sorted[half_index:]

        gem = median(half_lijst)
        return float(gem)


def var(lst):
    """ Retourneer de variantie (float) van de lijst lst. """
    gem = mean(lst)
    som_kwadraat = 0
    for nr in lst:
        verschil = nr - gem
        kwadraat = verschil ** 2
        som_kwadraat += kwadraat
    return som_kwadraat / len(lst)


def std(lst):
    """ Retourneer de standaardafwijking (float) van de lijst lst. """
    variant = var(lst)
    return variant ** 0.5


def freq(lst):
    """
    Retourneer een dictionary met als keys de waardes die voorkomen in lst en
    als value het aantal voorkomens van die waarde.
    Examples:
        freq([0, 0, 4, 5])
        {0: 2, 4: 1, 5: 1}
    """
    sort = sorted(lst)
    freqs = dict()
    for i in sort:
        counter = 0
        for n in lst:
            if i == n:
                counter += 1
                freqs[i] = counter
    return freqs


def modes(lst):
    """ Retourneer een gesorteerde lijst (list) van de modi van lijst lst. """

    modi = []
    fr = freq(lst)
    sort = sorted(fr.values(), reverse=True)

    for nr, frec in fr.items():
        if frec == sort[0]:
            modi.append(nr)
    return sorted(modi)


def ratings():
    data = Data.get_json()
    negative_ratings = []
    positive_ratings = []
    for ratings in range(0, len(data)):
        negative = data[ratings]["negative_ratings"]
        negative_ratings.append(negative)

    for ratings in range(0, len(data)):
        positive = data[ratings]["positive_ratings"]
        positive_ratings.append(positive)

    totaal_negatief = 0
    for neg_rating in negative_ratings:
        totaal_negatief += neg_rating

    totaal_positief = 0
    for pos_rating in positive_ratings:
        totaal_positief += pos_rating
    conclusie = f'Er zijn aanzienlijk veel meer positieve revieuws dan negatieve.\n' \
                f'De negatieve revieuws maken{int(totaal_negatief / (totaal_positief + totaal_negatief) * 100)}% uit van het totaal\n' \
                f'Er Kan dus gezegd worden dat de negatieve revieuws relatief\n minder zijn dan de positieve revieuws \n' \
                f'op steam.\n\n' \
                f'Enkele Statistieke cijfers met betrekking tot de\n negatieve en positieve revieuws.\n' \
                f'totaal aantal positieve reviews:{totaal_positief}\n' \
                f'gemmiddelde van het aantal\n positieve revieuws:{int(mean(positive_ratings))}\n' \
                f'kwartiel 1 van de positiece revieuws{q1(positive_ratings)}\n' \
                f'mediaan van de positieve revieuws{median(positive_ratings)}\n' \
                f'kwartiel 3 van de positieve reviews{q3(positive_ratings)}\n' \
                f'meest voorkomende aantal(modus)\n van de positieve revieuws{modes(positive_ratings)}\n' \
                f'Variatie van de positieve reviews {int(var(positive_ratings))}\n' \
                f'Standaard afwijking van de positieve reviews{int(std(positive_ratings))}\n' \
                f'totaal aantal negatieve reviews:{totaal_negatief}\n' \
                f'' \
                f'gemmiddelde van het aantal\n negatieve reviews:{int(mean(negative_ratings))}\n' \
                f'Kwartiel 1 van de negatieve reviews:{q1(negative_ratings)}\n' \
                f'Mediaan van de negatieve reviews:\n{median(negative_ratings)}\n' \
                f'Kwartiel 3 van de negatieve reviews:{q3(negative_ratings)}\n' \
                f'meest voorkomende aantal(modus)\n negatieve reviews:{modes(negative_ratings)}\n' \
                f'Variatie van de negatieve reviews:{int(var(negative_ratings))}\n' \
                f'Standaard afwijking van de negatieve reviews:{int(std(negative_ratings))}\n'

    return conclusie, totaal_negatief, totaal_positief


def platforms():
    data = Data.get_json()
    windows = 0
    windows_mac = 0
    windows_linux = 0
    windows_mac_linux = 0
    mac = 0
    linux = 0

    for platform in range(0, len(data)):
        platf = data[platform]["platforms"]
        if platf == "windows":
            windows += 1

    for platform in range(0, len(data)):
        platf = data[platform]["platforms"]
        if platf == "windows;mac":
            windows_mac += 1

    for platform in range(0, len(data)):
        platf = data[platform]["platforms"]
        if platf == "windows;mac;linux":
            windows_mac_linux += 1

    for platform in range(0, len(data)):
        platf = data[platform]["platforms"]
        if platf == "windows;linux":
            windows_linux += 1

    for platform in range(0, len(data)):
        platf = data[platform]["platforms"]
        if platf == "linux":
            linux += 1

    for platform in range(0, len(data)):
        platf = data[platform]["platforms"]
        if platf == "mac":
            mac += 1

    conclusie = f'Totaal aantal games: {len(data)}\n' \
                f'Aantal games beschikbaar op alleen windows:{windows}\n' \
                f'Aantal games beschikbaar op alleen mac:{mac}\n' \
                f'Aantal games beschikbaar op alleen linux:{linux}\n' \
                f'Aantal games beschikbaar op alleen windows en mac:{windows_mac}\n' \
                f'Aantal games beschikbaar op alleen windows en linux:{windows_linux}\n' \
                f'Aantal games beschikbaar op windows, mac en linux:{windows_mac_linux}\n' \
                f'De meeste games zijn op steam alleen voor winows.'
    return conclusie
