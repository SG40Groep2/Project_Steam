from tkinter import *
from Steam_Dashboard import *
import threading


venster = Tk(':0.0')
venster.title('steamdashboard')
venster.config(background='#1b2838')
venster.geometry("600x600")

opties_frame = Frame(venster)

opties_frame.pack(expand=True, fill='both')

profiel_frame = Frame(venster)

profiel_frame.pack(expand=True, fill='both')

statics_frame = Frame(venster)

statics_frame.pack(expand=True, fill='both')

hoofd_paneel = PanedWindow(venster, bd=4, relief=RAISED)

hoofd_paneel.pack(fill=BOTH, expand=1)

Online_mensen_frame = Frame(venster, bg='#1b2838')

Online_mensen_frame.pack(expand=True, fill='both')

vrienden = PanedWindow(hoofd_paneel, bd=4, relief=RAISED, orient=VERTICAL, bg='#1b2838')

populair = Label(vrienden, text='populair',anchor=N, bg='#1b2838', fg='#c7d5e0')

data = Data.get_profile_info()['response']['players'][0]['personaname']
text = f'vrienden\n\n{data}'
label = Label(text=text, fg='white', bg='#2a475e')


def verberg_alle_frames():
    for child in opties_frame.winfo_children():
        child.destroy()
    for child in profiel_frame.winfo_children():
        child.destroy()
    for child in statics_frame.winfo_children():
        child.destroy()
    for child in Online_mensen_frame.winfo_children():
        child.destroy()
    for child in hoofd_paneel.winfo_children():
        hoofd_paneel.remove(child)
    opties_frame.pack_forget()
    hoofd_paneel.pack_forget()
    statics_frame.pack_forget()
    profiel_frame.pack_forget()
    Online_mensen_frame.pack_forget()



def menu():
    hoofdmenu = Menu(venster)
    venster.config(menu=hoofdmenu)
    hoofdmenu.add_command(label='dashboard', command=dashboard)
    hoofdmenu.add_command(label='profiel', command=profile)
    hoofdmenu.add_command(label='statistics', command=statistics)
    hoofdmenu.add_command(label='opties', command=opties)
    hoofdmenu.add_command(label='online mensen', command=mensen_online)


def dashboard():
    verberg_alle_frames()
    hoofd_paneel.pack(fill=BOTH, expand=1)

    hoofd_paneel_text = Label(hoofd_paneel, text=f'aanbevolen voor jouw\n\n{aanbevolen_game}', anchor=N, bg='#1b2838', fg='#c7d5e0')
    hoofd_paneel.add(hoofd_paneel_text)

    vrienden.add(label)
    vrienden.add(populair)

    hoofd_paneel.add(vrienden)


def profile():
    verberg_alle_frames()
    profiel_frame.pack()
    Label(profiel_frame, text='profiel hier', bg='#c7d5e0').pack()

def statistics():
    verberg_alle_frames()
    statics_frame.pack()
    Label(statics_frame, text='statistics hier', bg='#c7d5e0').pack()

def opties():
    verberg_alle_frames()
    opties_frame.pack()
    Label(opties_frame, text='opties', bg='#c7d5e0').pack()

def mensen_online():
    verberg_alle_frames()
    Online_mensen_frame.pack()
    lege_ruimte = Label(Online_mensen_frame, text='', bg='#1b2838', fg='#c7d5e0',font=('Helvetica', 7, 'bold italic'))
    lege_ruimte.grid(row=0, column = 0)

    info_1 = Label(Online_mensen_frame, text=f'Steamid: "{data_knop[0][0]}"\n\n'
                                             f'Naam: {data_knop[0][1]}\n\n'
                                             f'Status: {data_knop[0][2]}',font=('Helvetica', 12, 'bold italic'), justify=LEFT, bg='#1b2838',fg='#c7d5e0')
    info_1.grid(row=1,column= 2)
    profielfoto_1 = Label(Online_mensen_frame, image=data_knop[0][3], anchor=W, bg='#1b2838', fg='#c7d5e0')
    profielfoto_1.grid(row=1,column=0, ipadx = 30)

    info_2 = Label(Online_mensen_frame, text=f'steamid2: "{data_knop[1][0]}"\n\n'
                                             f'naam2: {data_knop[1][1]}\n\n'
                                             f'status2: {data_knop[1][2]}',font=('Helvetica', 12, 'bold italic'), justify=LEFT, bg='#1b2838', fg='#c7d5e0')
    info_2.grid(row=2,column=2)
    profielfoto_2 = Label(Online_mensen_frame, image=data_knop[1][3], anchor=W, bg='#1b2838', fg='#c7d5e0')
    profielfoto_2.grid(row=2,column=0, ipadx = 30)

    info_3 = Label(Online_mensen_frame, text=f'steamid3: "{data_knop[2][0]}"\n\n'
                                             f'naam3: {data_knop[2][1]}\n\n'
                                             f'status3: {data_knop[2][2]}',font=('Helvetica', 12, 'bold italic'), justify=LEFT, bg='#1b2838', fg='#c7d5e0')
    info_3.grid(row=3,column=2)
    profielfoto_3 = Label(Online_mensen_frame, image=data_knop[2][3], anchor=W, bg='#1b2838', fg='#c7d5e0')
    profielfoto_3.grid(row=3,column=0, ipadx = 30)


def opstarten():
    leuke_dingen_uitprinten()
    menu()
    dashboard()
    thread1.start()
    thread2.start()
    thread3.start()
    # venster.update()
    while True:
        if GPIO.input(switch1):
            print('knop is ingedrukt!')
            mensen_online()
            venster.update()
            time.sleep(0.5)
        else:
            venster.update()



thread1 = threading.Thread(target=sr04, args=(sr04_trig, sr04_echo, pieper))
thread2 = threading.Thread(target=Data.gedachte_neopixels)
thread3 = threading.Thread(target= Data.gemiddeld_procent)


data_knop = Data.verwerk_online_info()
aanbevolen_game = Data.sort_json(Data.get_json())[0]['name'] #naam van de aanbevolen game

opstarten()



