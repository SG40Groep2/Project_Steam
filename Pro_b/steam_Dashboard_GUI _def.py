from tkinter import *
from Steam_Dashboard_def import *
from Steam_dashboard_api import *
from Steam_dashboard_statistics import *
# from SR04_Servo_piep_steam import *
# from HC595_steam import *
import threading
import tkinter.scrolledtext as st


back_ground = '#1b2838'
fore_ground = '#c7d5e0'

venster = Tk(':0.0')
venster.title('steamdashboard')
venster.config(background=back_ground)
venster.resizable(False,False)
venster.geometry("600x600")


statics_frame = Frame(venster)

statics_frame.pack(fill='both', expand=True)

Online_mensen_frame = Frame(venster, bg=back_ground)

Online_mensen_frame.pack(expand=True, fill='both')

dashboard_frame = Frame(venster, bg=back_ground)

dashboard_frame.pack(fill='both', expand=True)



def verberg_alle_frames():
    for child in statics_frame.winfo_children():
        child.destroy()
    for child in dashboard_frame.winfo_children():
        child.destroy()
    for child in Online_mensen_frame.winfo_children():
        child.destroy()

    dashboard_frame.pack_forget()
    statics_frame.pack_forget()
    Online_mensen_frame.pack_forget()


def menu():
    hoofdmenu = Menu(venster)
    venster.config(menu=hoofdmenu)
    hoofdmenu.add_command(label='dashboard', command=dashboard)
    hoofdmenu.add_command(label='statistics', command=statistics_ratings)
    hoofdmenu.add_command(label='online mensen', command=mensen_online)


def game_screen():
    gamescreen = Tk()
    get = searchbar.get()
    gamescreen.title(f'{get}')
    gamescreen.config(background=back_ground)
    gamescreen.resizable(False, False)
    gamescreen.geometry("300x300")
    game_ind = found[1]

    text = f'{get}\n\n\n\n\n\n' \
           f'release date:{Data.get_json()[game_ind]["release_date"]}\n\n' \
           f'developer: {Data.get_json()[game_ind]["developer"]}\n\n' \
           f'uitgever:   {Data.get_json()[game_ind]["publisher"]}\n\n' \
           f'platformen:   {Data.get_json()[game_ind]["platforms"]}\n\n' \
           f'leeftijd:  {Data.get_json()[game_ind]["required_age"]}\n\n' \
           f'genre:   {Data.get_json()[game_ind]["genres"]}'

    title = Label(gamescreen, text=text, bg=back_ground, fg=fore_ground)
    title.pack()

    venster.update()



def game_search(canvas):
    global searchbar
    canvas.create_text(450, 85, text='Zoek hier naar Jouw Favoriete games!', fill=fore_ground, font=25)
    searchbar = Entry(dashboard_frame, width=35)
    wind_search = canvas.create_window(450, 140, height=25, width=200)
    canvas.itemconfigure(wind_search, window=searchbar)

    zoek = Button(dashboard_frame, text='zoek',
                  command=search_implement, bg=back_ground,
                  fg=fore_ground)




    wind_but = canvas.create_window(450, 180, height=20, width=50)
    canvas.itemconfigure(wind_but, window=zoek)


def search_implement():
    global found
    arr = Data.get_json()
    found = Search(arr).binary_search(searchbar.get(), 'name')
    if found:
        game_screen()
    else:
        text = 'We hebben geen resultaten voor jouw zoek opdracht.\n' \
               'Controleer of je het goed hebt geschreven',
        canvas_2.create_text(450, 235, text=text, fill='red')



def aanb_text(json, canvas_1):
    h = 110
    for game in range(0, len(json)):
        h += 20
        aanbev_text = Label(text=f"{json[game]['name']} €{json[game]['price']}", bg=back_ground, fg=fore_ground)

        wind = canvas_1.create_window(120, h, height=25, width=200)
        canvas_1.itemconfigure(wind, window=aanbev_text)


def pop_text(json, canvas_2):
    o = 60
    for game in range(0, 6):  # games
        o += 25
        populair = Label(text=f"{json[game]['name']} €{json[game]['price']}", bg=back_ground,
                         fg=fore_ground)

        wind = canvas_2.create_window(145, o, height=25, width=275)
        canvas_2.itemconfigure(wind, window=populair)





def dashboard():
    """bron: https://www.geeksforgeeks.org/python-tkinter-scrolledtext-widget/"""

    verberg_alle_frames()
    dashboard_frame.pack()

    aanbevolen_json = Data.get_json()[2500:2506]
    populaire_json = Data.get_json()[116:122]


    # lijst met opties
    optionlist = ['positieve ratings', 'negatieve ratings', 'prijs']
    pos = Sort(aanbevolen_json).my_insertion_sort(key="positive_ratings")
    naam = Sort(aanbevolen_json).my_insertion_sort(key="name")
    pr = Sort(aanbevolen_json).my_insertion_sort(key='price')

    pos_pop = Sort(populaire_json).my_insertion_sort(key="positive_ratings")
    name_pop = Sort(populaire_json).my_insertion_sort(key="name")
    pr_pop =  Sort(populaire_json).my_insertion_sort(key="price")

    # canvas waar dashboard op zit
    canvas_1 = Canvas(dashboard_frame, width=600, height=280, bg='#1b2838')
    canvas_1.create_line(0, 280, 600, 280, fill=fore_ground, width=4)
    canvas_1.create_line(245, 0, 245, 280, fill=fore_ground, width=4)

    # text met scrollbar voor vrienden
    canvas_1.create_text(450, 15, text='Vrienden', font=35, fill='#c7d5e0')
    scroll_text = st.ScrolledText(dashboard_frame, bg=back_ground, fg=fore_ground, width=85, height=80)
    for friends in data_knop:
        vriend = f'{friends[1]}({friends[2]})\n'

        scroll_text.insert(INSERT, vriend)

    scroll_text.pack()
    scroll_text.configure(state='disabled')
    wind = canvas_1.create_window(450, 65, height=80, width=200)
    canvas_1.itemconfigure(wind, window=scroll_text)

    # text met scrollbar voor gebruiker games
    canvas_1.create_text(450, 145, text='Jouw Games', font=35, fill=fore_ground)
    scroll_text_game = st.ScrolledText(dashboard_frame, bg=back_ground, fg=fore_ground, width=350, height=80)
    my_games = app.owned_games(ahmed_id)
    lst = my_games["response"]["games"]
    it = 0

    for i in lst:
        games = f'{lst[it]["name"]}\n'
        it += 1
        scroll_text_game.insert(INSERT, games)

    scroll_text_game.pack()
    scroll_text_game.configure(state='disabled')
    wind_games = canvas_1.create_window(420, 205, height=80, width=300)
    canvas_1.itemconfigure(wind_games, window=scroll_text_game)

    # aanbevolen games:
    hoofd_paneel_text = 'aanbevolen voor jou:'  # titel
    canvas_1.create_text(125, 15, text=hoofd_paneel_text, fill=fore_ground)

    # knoppen voor aanbevolen

    knop_az = Button(dashboard_frame, text='A-Z', bg=back_ground, fg=fore_ground, width=20,  # knop om te sorteren op naam
                     command=lambda: aanb_text(naam, canvas_1))  # knop om te sorteren op naam
    wind_az = canvas_1.create_window(125, 50, height=25, width=105)  # knop om te sorteren op naam
    canvas_1.itemconfigure(wind_az, window=knop_az)  # knop om te sorteren op naam

    knop_pos_a = Button(dashboard_frame, text='positieve ratings', bg=back_ground, fg=fore_ground, width=20,
                        # knop om te sorteren op positieve ratings
                        command=lambda: aanb_text(pos, canvas_1))  # knop om te sorteren op positieve ratings
    wind_pos_a = canvas_1.create_window(125, 70, height=25, width=105)  # knop om te sorteren op positieve ratings
    canvas_1.itemconfigure(wind_pos_a, window=knop_pos_a)  # knop om te sorteren op positieve ratings

    knop_pr_a = Button(dashboard_frame, text='prijs', bg=back_ground, fg=fore_ground, width=20,  # knop om te sorteren op
                       # prijs
                       command=lambda: aanb_text(pr, canvas_1))  # knop om te sorteren op prijs
    wind_pr_a = canvas_1.create_window(125, 90, height=25, width=105)  # knop om te sorteren op prijs
    canvas_1.itemconfigure(wind_pr_a, window=knop_pr_a)  # knop om te sorteren op prijs

    # ander canvas waar 'populaire' games worden getoond'
    global canvas_2
    canvas_2 = Canvas(dashboard_frame, width=600, height=340, bg=back_ground)
    populair = 'populair'  # titel
    canvas_2.create_text(145, 50, text=populair, font=35, fill=fore_ground)

    pop_text(populaire_json, canvas_2)
    game_search(canvas_2)

    # knoppen voor populair

    knop_pos = Button(dashboard_frame, text='positieve ratings', bg=back_ground, fg=fore_ground, width=105,
                      # knop om te sorteren op positieve ratings
                      command=lambda: pop_text(pos_pop, canvas_2))  # knop om te sorteren op positieve ratings
    wind_pos = canvas_2.create_window(70, 15, height=20, width=105)  # knop om te sorteren op positieve ratings
    canvas_2.itemconfigure(wind_pos, window=knop_pos)  # knop om te sorteren op positieve ratings

    knop_name = Button(dashboard_frame, text='A-Z', bg=back_ground, fg=fore_ground, width=105,
                       # knop om te sorteren op naam
                       command=lambda: pop_text(name_pop, canvas_2))  # knop om te sorteren op naam
    wind_name = canvas_2.create_window(170, 15, height=20, width=105)  # knop om te sorteren op naam
    canvas_2.itemconfigure(wind_name, window=knop_name)  # knop om te sorteren op naam

    knop_pr = Button(dashboard_frame, text='prijs', bg=back_ground, fg=fore_ground, width=105,
                     # knop om te sorteren op prijs
                     command=lambda: pop_text(pr_pop, canvas_2))  # knop om te sorteren op prijs
    wind_pr = canvas_2.create_window(270, 15, height=20, width=105)  # knop om te sorteren op prijs
    canvas_2.itemconfigure(wind_pr, window=knop_pr)  # knop om te sorteren op prijs

    aanb_text(aanbevolen_json, canvas_1)

    canvas_1.pack()
    canvas_2.pack()


def statistics_ratings():
    verberg_alle_frames()
    statics_frame.pack()
    can = Canvas(statics_frame, width=600, height=600, bg=back_ground)

    titel_ratings = Label(statics_frame, text='Ratings op steam', bg=back_ground, fg=fore_ground)
    wind = can.create_window(185, 10, height=10, width=105)
    can.itemconfigure(wind, window=titel_ratings)

    conclusie = Label(statics_frame, text=ratings()[0], bg=back_ground, fg=fore_ground)
    wind_con = can.create_window(185, 275, height=500, width=350)
    can.itemconfigure(wind_con, window=conclusie)

    switch = Button(statics_frame, text='Platforms', bg=back_ground, fg=fore_ground,width=45, command=statistics_platforms)
    wind_switch = can.create_window(185, 550, height=25, width=90)
    can.itemconfigure(wind_switch, window=switch)
    can.pack()




def statistics_platforms():
    verberg_alle_frames()
    statics_frame.pack()
    can = Canvas(statics_frame, width=600, height=600, bg=back_ground)

    titel_platform = Label(statics_frame, text='Beschikbaarheid van games op verschillende platformen', bg=back_ground,
                           fg=fore_ground)
    wind_titel = can.create_window(300, 25, height=25, width=300)
    can.itemconfigure(wind_titel, window=titel_platform)

    conclusie_2 = Label(statics_frame, text=platforms(), bg=back_ground, fg=fore_ground)
    wind_conc2 = can.create_window(300, 125, height=120, width=385)
    can.itemconfigure(wind_conc2, window=conclusie_2)

    switch = Button(statics_frame, text='ratings', bg=back_ground, fg=fore_ground,width=45, command=statistics_ratings)
    wind_switch = can.create_window(60, 25, height=25, width=90)
    can.itemconfigure(wind_switch, window=switch)

    can.pack()




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

    info_2 = Label(Online_mensen_frame, text=f'steamid: "{data_knop[1][0]}"\n\n'
                                             f'naam: {data_knop[1][1]}\n\n'
                                             f'status: {data_knop[1][2]}', font=('Helvetica', 12, 'bold italic'),
                   justify=LEFT, bg='#1b2838', fg='#c7d5e0')
    info_2.grid(row=2, column=2)
    profielfoto_2 = Label(Online_mensen_frame, image=data_knop[1][3], anchor=W, bg='#1b2838', fg='#c7d5e0')
    profielfoto_2.grid(row=2, column=0, ipadx=30)

    info_3 = Label(Online_mensen_frame, text=f'steamid: "{data_knop[2][0]}"\n\n'
                                             f'naam: {data_knop[2][1]}\n\n'
                                             f'status: {data_knop[2][2]}', font=('Helvetica', 12, 'bold italic'),
                   justify=LEFT, bg='#1b2838', fg='#c7d5e0')
    info_3.grid(row=3, column=2)
    profielfoto_3 = Label(Online_mensen_frame, image=data_knop[2][3], anchor=W, bg='#1b2838', fg='#c7d5e0')
    profielfoto_3.grid(row=3, column=0, ipadx=30)


def opstarten():
    menu()
    dashboard()
    # thread_sr04.start()
    # thread_neopixel.start()
    # thread_hc595.start()
    # while True:
    #     if GPIO.input(switch1):
    #         print('knop is ingedrukt!')
    #         mensen_online()
    #         venster.update()
    #         time.sleep(0.5)
    #     else:
    #         venster.update()

# thread_sr04 = threading.Thread(target=sr04, args=(sr04_trig, sr04_echo, pieper))
# thread_neopixel = threading.Thread(target=Data.gedachte_neopixels)
# thread_hc595 = threading.Thread(target=achievenentleds)


data = app.get_profile_info(ahmed_id)['response']['players'][0]['personaname']
text = f'vrienden\n\n{data}'
label = Label(text=text, fg='white', bg='#2a475e')
data_knop = Data.verwerk_online_info()
# aanbevolen_game = Data.sort_json(Data.get_json())[0]['name']  # naam van de aanbevolen game

# leuke_dingen_uitprinten()

opstarten()
venster.mainloop()