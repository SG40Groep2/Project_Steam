from tkinter import *
from Steam_Dashboard import *
import tkinter.scrolledtext as st

# import threading

venster = Tk()
venster.title('steamdashboard')
venster.config(background='#1b2838')
venster.geometry("600x600")

games = Frame(venster, bg='#1b2838')

games.pack(fill='both', expand=True)

profiel_frame = Frame(venster)

profiel_frame.pack(fill='both', expand=True)

statics_frame = Frame(venster)

Online_mensen_frame = Frame(venster, bg='#1b2838')

Online_mensen_frame.pack(expand=True, fill='both')

statics_frame.pack(fill='both', expand=True)

dashboard_frame = Frame(venster, bg='#1b2838')

dashboard_frame.pack(fill='both', expand=True)


def verberg_alle_frames():
    for child in games.winfo_children():
        child.destroy()
    for child in profiel_frame.winfo_children():
        child.destroy()
    for child in statics_frame.winfo_children():
        child.destroy()
    for child in dashboard_frame.winfo_children():
        child.destroy()
    for child in Online_mensen_frame.winfo_children():
        child.destroy()

    games.pack_forget()
    dashboard_frame.pack_forget()
    statics_frame.pack_forget()
    profiel_frame.pack_forget()
    Online_mensen_frame.pack_forget()


def menu():
    hoofdmenu = Menu(venster)
    venster.config(menu=hoofdmenu)
    hoofdmenu.add_command(label='dashboard', command=dashboard)
    hoofdmenu.add_command(label='games', command=library)
    hoofdmenu.add_command(label='statistics', command=statistics)
    hoofdmenu.add_command(label='online mensen', command=mensen_online)


def aanb_text(aanbevolen_json, canvas_1):
    h = 110
    for game in range(0, len(aanbevolen_json)):
        h += 20
        aanbev_text = Label(text=aanbevolen_json[game]['name'], bg='#1b2838', fg='#c7d5e0')
        aanbev_text.config(text=aanbevolen_json[game]['name'])
        wind = canvas_1.create_window(120, h, height=25, width=200)
        canvas_1.itemconfigure(wind, window=aanbev_text)


def pop_text(populaire_json, canvas_2):
    o = 60
    for game in range(0, 6):  # games
        o += 25
        populair = Label(text=f"{populaire_json[game]['name']} €{populaire_json[game]['price']}", bg='#1b2838',
                         fg='#c7d5e0')
        populair.config(text=populaire_json[game]['name'])
        wind = canvas_2.create_window(300, o, height=25, width=200)
        canvas_2.itemconfigure(wind, window=populair)


def game_search():
    searchbar = Entry(dashboard_frame, width=35)
    # searchbar.delete(0, END)
    target = searchbar.get()
    print(target)
    found = Algo.linear_search(Data.get_json(), target, 'name')
    zoek = Button(dashboard_frame, text='zoek', command=lambda:print(found))
    zoek.pack(anchor=E)
    searchbar.pack(anchor=E)




def dashboard():
    """bron: https://www.geeksforgeeks.org/python-tkinter-scrolledtext-widget/"""

    global knop, aanbev_text
    verberg_alle_frames()
    dashboard_frame.pack()

    game_search()

    aanbevolen_json = Data.get_json()[0:6]
    populaire_json = Data.get_json()[200:206]
    data = Data.get_profile_info(key, ahmed_id)['response']['players'][0]['personaname']
    friends = f'  {data}(offline)'

    # lijst met opties
    optionlist = ['A-Z', 'Z-A', 'prijs, hoog-laag', 'prijs, laag-hoog']
    a_z = Algo.my_insertion_sort(steam=aanbevolen_json, key='name', reverse=False)
    z_a = Algo.my_insertion_sort(steam=aanbevolen_json, key='name', reverse=True)
    pr_la_ho = Algo.my_insertion_sort(steam=aanbevolen_json, key='price', reverse=False)
    pr_ho_la = Algo.my_insertion_sort(steam=aanbevolen_json, key='price', reverse=True)

    a_z_pop = Algo.my_insertion_sort(steam=populaire_json, key='name', reverse=False)
    z_a_pop = Algo.my_insertion_sort(steam=populaire_json, key='name', reverse=True)
    pr_la_ho_pop = Algo.my_insertion_sort(steam=populaire_json, key='price', reverse=False)
    pr_ho_la_pop = Algo.my_insertion_sort(steam=populaire_json, key='price', reverse=True)

    button_command = [a_z, z_a, pr_ho_la, pr_la_ho]

    button_command_pop = [a_z_pop, z_a_pop, pr_ho_la_pop, pr_la_ho_pop]

    # canvas waar dashboard op zit
    canvas_1 = Canvas(dashboard_frame, width=600, height=280, bg='#1b2838')
    canvas_1.create_line(0, 280, 600, 280, fill='#c7d5e0', width=4)
    canvas_1.create_line(245, 0, 245, 280, fill='#c7d5e0', width=4)

    # text met scrollbar voor vrienden
    canvas_1.create_text(450, 15, text='Vrienden', font=35, fill='#c7d5e0')
    scroll_text = st.ScrolledText(dashboard_frame, bg='#1b2838', fg='#c7d5e0', width=85, height=80)
    scroll_text.insert(INSERT, friends)
    scroll_text.pack()
    scroll_text.configure(state='disabled')
    wind = canvas_1.create_window(450, 65, height=80, width=200)
    canvas_1.itemconfigure(wind, window=scroll_text)

    # aanbevolen games:
    hoofd_paneel_text = 'aanbevolen voor jouw:'  # titel
    canvas_1.create_text(175, 15, text=hoofd_paneel_text, fill='#c7d5e0')
    h = 35

    aanb_text(aanbevolen_json, canvas_1)

    # knoppen voor aanbevolen
    l = 50
    y = 15
    for i in optionlist:
        # l += 85
        y += 20
        comm_index = optionlist.index(i)
        knop = Button(dashboard_frame, text=i, bg='#1b2838', fg='#c7d5e0', width=len(i),
                      command=lambda: aanb_text(button_command[comm_index], canvas_1))
        wind = canvas_1.create_window(l, y, height=25, width=85)
        canvas_1.itemconfigure(wind, window=knop)

    hoofd_paneel_text = f'aanbevolen voor jouw'

    # ander canvas waar 'populaire' games worden getoond'
    canvas_2 = Canvas(dashboard_frame, width=600, height=340, bg='#1b2838')
    populair = 'populair'  # titel
    canvas_2.create_text(300, 60, text=populair, font=35, fill='#c7d5e0')

    pop_text(populaire_json, canvas_2)

    m = 40
    # knoppen voor populair
    for i in optionlist:
        m += 85
        comm_index = optionlist.index(i)
        knop = Button(dashboard_frame, text=i, bg='#1b2838', fg='#c7d5e0', width=len(i),
                      command=lambda: pop_text(button_command_pop[comm_index], canvas_2))
        wind = canvas_2.create_window(m, 15, height=25, width=85)
        canvas_2.itemconfigure(wind, window=knop)

    # knoppen voor vrienden sorteren
    l = 300
    y = 15
    friend_commands = []
    sort1 = 'placeholder'
    sort2 = 'placeholder'
    for i in optionlist[0:2]:
        y += 20
        knop = Button(dashboard_frame, text=i, bg='#1b2838', fg='#c7d5e0', width=len(i))
        wind = canvas_1.create_window(l, y, height=25, width=85)
        canvas_1.itemconfigure(wind, window=knop)

    canvas_1.pack()
    canvas_2.pack()


def library():
    verberg_alle_frames()
    games.pack()

    # owned_games = Label(games, text='this is a placeholder', bg='#c7d5e0')
    # owned_games.pack()


def statistics():
    verberg_alle_frames()
    statics_frame.pack()
    Label(statics_frame, text='statistics hier', bg='#c7d5e0').pack()


def mensen_online():
    verberg_alle_frames()
    Online_mensen_frame.pack()
    lege_ruimte = Label(Online_mensen_frame, text='', bg='#1b2838', fg='#c7d5e0', font=('Helvetica', 7, 'bold italic'))
    lege_ruimte.grid(row=0, column=0)

    info_1 = Label(Online_mensen_frame, text=f'Steamid: "{data_knop[0][0]}"\n\n'
                                             f'Naam: {data_knop[0][1]}\n\n'
                                             f'Status: {data_knop[0][2]}', font=('Helvetica', 12, 'bold italic'),
                   justify=LEFT, bg='#1b2838', fg='#c7d5e0')
    info_1.grid(row=1, column=2)
    profielfoto_1 = Label(Online_mensen_frame, image=data_knop[0][3], anchor=W, bg='#1b2838', fg='#c7d5e0')
    profielfoto_1.grid(row=1, column=0, ipadx=30)

    info_2 = Label(Online_mensen_frame, text=f'steamid2: "{data_knop[1][0]}"\n\n'
                                             f'naam2: {data_knop[1][1]}\n\n'
                                             f'status2: {data_knop[1][2]}', font=('Helvetica', 12, 'bold italic'),
                   justify=LEFT, bg='#1b2838', fg='#c7d5e0')
    info_2.grid(row=2, column=2)
    profielfoto_2 = Label(Online_mensen_frame, image=data_knop[1][3], anchor=W, bg='#1b2838', fg='#c7d5e0')
    profielfoto_2.grid(row=2, column=0, ipadx=30)

    info_3 = Label(Online_mensen_frame, text=f'steamid3: "{data_knop[2][0]}"\n\n'
                                             f'naam3: {data_knop[2][1]}\n\n'
                                             f'status3: {data_knop[2][2]}', font=('Helvetica', 12, 'bold italic'),
                   justify=LEFT, bg='#1b2838', fg='#c7d5e0')
    info_3.grid(row=3, column=2)
    profielfoto_3 = Label(Online_mensen_frame, image=data_knop[2][3], anchor=W, bg='#1b2838', fg='#c7d5e0')
    profielfoto_3.grid(row=3, column=0, ipadx=30)


def opstarten():
    # leuke_dingen_uitprinten()
    menu()
    dashboard()
    # thread1.start()
    # thread2.start()
    # thread3.start()
    # venster.update()


#     while True:
#         if GPIO.input(switch1):
#             print('knop is ingedrukt!')
#             mensen_online()
#             venster.update()
#             time.sleep(0.5)
#         else:
#             venster.update()
#
#
#
# thread1 = threading.Thread(target=Data.sr04, args=(sr04_trig, sr04_echo, pieper))
# thread2 = threading.Thread(target=Data.gedachte_neopixels)
# thread3 = threading.Thread(target= Data.gemiddeld_procent)

data_knop = Data.verwerk_online_info()
# aanbevolen_game = Data.sort_json(Data.get_json())[0]['name'] #naam van de aanbevolen game

opstarten()

venster.mainloop()
