import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def on_exit():
    # demander confirmation puis fermer la fenêtre
    if messagebox.askokcancel("Quitter", "Voulez-vous quitter le jeu ?"):
        fenetre.destroy()

def sure():
    frame1.pack_forget()
    frame2.pack()

#FENETRE
fenetre = tk.Tk()
fenetre.title('Bataille navale')
fenetre.geometry('400x340')

#FRAME 1
frame1 = tk.Frame(fenetre)
frame1.pack()

# FRAME 1 (écran d'accueil)
frame1 = tk.Frame(fenetre)
frame1.pack(fill='both', expand=True)

# Style pour bouton plus grand (hauteur via padding + police)
style = ttk.Style()
style.configure('Big.TButton', font=('Helvetica', 16, 'bold'), padding=(20, 12))

# Bouton simple et centré (dans frame1)
button = ttk.Button(frame1, text='Start Game', style='Big.TButton')
button.pack(padx=10, pady=20)

# FRAME 2 (contenu principal, non packé au démarrage)
frame2 = tk.Frame(fenetre)
tk.Label(frame2, text="Bienvenue dans la Bataille Navale!", font=('Klee', 14, 'bold')).pack(pady=10)
back_btn = ttk.Button(frame2, text='Retour', command=lambda: (frame2.pack_forget(), frame1.pack(fill='both', expand=True)))
back_btn.pack(pady=5)

fenetre.protocol("WM_DELETE_WINDOW", on_exit)

# lier le bouton d'accueil à la fonction qui affiche frame2
button.config(command=sure)

#run 
fenetre.mainloop()