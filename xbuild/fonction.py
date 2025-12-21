import tkinter as tk
from tkinter.messagebox import showinfo

def swap_frames(hide, show):
    """Echanger un frame en arrière-plan et un frame au premier plan.
    .pack_forget() sert à cacher un frame
    .pack() sert à afficher un frame
    """
    hide.pack_forget()
    show.pack(fill='both', expand=True)

# BOUTON PERSONNALISÉ 
def bouton(parent, text_lines, wid, hei, size1, size2, boldd, relly, command=None):
    """
    parent: frame parent
    text_lines: text à afficher (liste de lignes)
    wid: longueur du bouton
    hei: hauteur du bouton
    size1: taille du texte principal
    size2: taille du texte secondaire
    command: lier la fonction et l'action 'le bouton est cliqué'

    .winfo_children() retourne la liste des widgets enfants d'un widget parent
    .bind() lie un événement (ici clic gauche) à une fonction
    """
    btn = tk.Frame(parent, width=wid, height=hei, bd=2, relief='raised')
    btn.place(relx=0.5, rely= relly, anchor='center'); btn.pack_propagate(False)
    for line in text_lines:
        if text_lines[1] == line:
            tk.Label(btn, text=line, font=('Helvetica',size1,boldd)).pack()
        else:
            tk.Label(btn, text=line, font=('Helvetica',size2)).pack()
    if command:
        def _on_click(event, cmd=command):
            """
            event: evenement (ex. clic gauche)
            cmd: fonction à appeler
            _on_click c'est si on clique sur le bouton 
            """
            cmd()
        for w in btn.winfo_children():
            w.bind('<Button-1>', _on_click)
        btn.bind('<Button-1>', _on_click)
    return btn

#BARRE DE MENU
def create_menu(fenetre):
    """
    fenetre: fenetre principale
    """
    def alert():
        showinfo("alerte", "Bravo!")  
        
    menubar = tk.Menu(fenetre)

    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label="Nouvelle partie contre une ia", command=alert)
    menu1.add_command(label="Nouvelle partie contre un joueur", command=alert)
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=fenetre.quit)
    menubar.add_cascade(label="Game", menu=menu1)

    menu2 = tk.Menu(menubar, tearoff=0)
    menu2.add_command(label="Regles du jeu", command=alert)
    menu2.add_command(label="A propos", command=alert)
    menubar.add_cascade(label="Help", menu=menu2)

    fenetre.config(menu=menubar)

# PANNEAUX
def panel(p, wid, hei, bg_color, content):
    panel = tk.Frame(p, width=wid, height=hei, background=bg_color)
    panel.pack_propagate(False)
    tk.Label(panel, text=content, background=bg_color).pack(expand=True)
    return panel