# coding: utf-8
 
import tkinter as tk
from tkinter import ttk
import os
from tkinter.messagebox import showinfo

#FENETRE
fenetre = tk.Tk()
fenetre.title('Bataille navale')
fenetre.geometry('600x600')

#barre de menu 
def alert():
    showinfo("alerte", "Bravo!")

menubar = tk.Menu(fenetre)

menu1 = tk.Menu(menubar, tearoff=0)
menu1.add_command(label="Nouvelle partie contre une ia", command=alert)
menu1.add_command(label="Nouvelle partie contre un joueur", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = tk.Menu(menubar, tearoff=0)
menu2.add_command(label="Regles du jeu", command=alert)
menu2.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu2)

fenetre.config(menu=menubar)

#IMAGES
HERE = os.path.dirname(__file__)
IMG_PATH = os.path.normpath(os.path.join(HERE, '..', 'images', 'Icône de bateau.png'))
# Charger et redimensionner l'image
img1 = tk.PhotoImage(file=IMG_PATH).subsample(25, 25)

#FRAME 1
frame1 = tk.Frame(fenetre)
frame1.pack()

#FRAME 2 
frame2 = tk.Frame(fenetre)
#frame2.pack()

#titre
titre_label = ttk.Label(frame1, text = 'Bataille Navale ;^;', font='Klee 24 bold')
titre_label.pack()

# input
input_frame = ttk.Frame(frame1)
entry = ttk.Entry(master=input_frame)
# bouton utilise la même alerte que le menu
button = ttk.Button(master=input_frame, text='Entrée', command=alert)
entry.pack(side='left', padx=10)
button.pack(side='left')
input_frame.pack(pady=10)

# panneau 
# Donner une taille fixe au PanedWindow et empêcher qu'il s'ajuste
# PanedWindow fixe
p = tk.PanedWindow(fenetre, orient=tk.HORIZONTAL, width=560, height=600)
# Empêche le PanedWindow de se redimensionner en fonction du contenu
p.pack_propagate(False)
p.pack(side=tk.TOP, pady=2, padx=2)

# Volet gauche — texte (taille fixe)
left = tk.Frame(p, width=120, height=200, background='#7d9ab5')
left.pack_propagate(False)
ttk.Label(left, text='Volet 2', background='#7d9ab5').pack(expand=True)
p.add(left)

# Volet droit — image (taille fixe)
right = tk.Frame(p, width=480, height=600, background='#97b3ce')
right.pack_propagate(False)
label_img = tk.Label(right, image=img1, background='#97b3ce')
label_img.image = img1
# placer l'image en haut à gauche du volet droit
label_img.pack(anchor='nw', padx=5, pady=5)
p.add(right)

#run 
fenetre.mainloop()

