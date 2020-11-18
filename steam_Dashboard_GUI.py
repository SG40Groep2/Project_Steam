from tkinter import *
from Steam_Dashboard import *


venster = Tk()
venster.title('steamdashboard')
venster.geometry("600x600")

def online_friends():
    return Label(text=f'online\n\n(Naam vriend) speelt {eerste_game}')

def dashboard():
    hoofd_paneel= PanedWindow(bd=4, relief=RAISED)
    hoofd_paneel.pack(fill=BOTH, expand=1)

    hoofd_paneel_text = Label(hoofd_paneel, text='aanbevolen voor jouw', anchor=N)
    hoofd_paneel.add(hoofd_paneel_text)

    vrienden_online = PanedWindow(hoofd_paneel, bd=4, relief=RAISED, orient=VERTICAL,bg='darkblue')

    vrienden_online.add(online_friends())

    populair = Label(vrienden_online, text='populair',anchor=N)
    vrienden_online.add(populair)
    hoofd_paneel.add(vrienden_online)

dashboard()

venster.mainloop()