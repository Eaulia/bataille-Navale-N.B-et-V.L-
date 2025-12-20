# coding: utf-8
 
import tkinter as tk 
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo

#fenetre
fenetre = tk.Tk()
fenetre.title('Bataille navale')
fenetre.geometry('600x600')

#barre de menu 
def alert():
    showinfo("alerte", "Bravo!")

menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouvelle partie contre une ia", command=alert)
menu1.add_command(label="Nouvelle partie contre un joueur", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Regles du jeu", command=alert)
menu2.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu2)

fenetre.config(menu=menubar)

#titre
titre_label = ttk.Label(master = fenetre, text = 'Bataille Navale ;^;', font='Klee 24 bold')
titre_label.pack()

#input field 
input_frame = ttk.Frame(master = fenetre)
entry = ttk.Entry(master = input_frame)
button = ttk.Button(master = input_frame, text= 'Entrée')
entry.pack(side = 'left', padx = 10)
button.pack(side = 'left')
input_frame.pack(pady = 10)

#panneau 
p = PanedWindow(fenetre, orient=HORIZONTAL)
p.pack(side=TOP, fill=BOTH, pady=2, padx=2)
p.add(Label(p, text='Volet 1', background='#97b3ce', padx= 50, pady=200))
p.add(Label(p, text='Volet 2', background='#7d9ab5'))
p.pack()

#run 
fenetre.mainloop()

