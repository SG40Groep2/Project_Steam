from tkinter import *
from Steam_Dashboard import *


venster = Tk()
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
    for child in hoofd_paneel.winfo_children():
        hoofd_paneel.remove(child)
    opties_frame.pack_forget()
    hoofd_paneel.pack_forget()
    hoofd_paneel.pack_forget()
    statics_frame.pack_forget()
    profiel_frame.pack_forget()



def menu():
    hoofdmenu = Menu(venster)
    venster.config(menu=hoofdmenu)
    hoofdmenu.add_command(label='dashboard', command=dashboard)
    hoofdmenu.add_command(label='profiel', command=profile)
    hoofdmenu.add_command(label='statistics', command=statistics)
    hoofdmenu.add_command(label='opties', command=opties)


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


menu()
dashboard()
venster.mainloop()