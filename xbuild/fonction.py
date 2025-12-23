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
    text_lines: texte à afficher (liste de lignes)
    wid: longueur du bouton
    hei: hauteur du bouton
    size1: taille du texte principal
    size2: taille du texte secondaire
    command: lier la fonction et l'action 'le bouton est cliqué'

    .winfo_children() retourne la liste des widgets enfants d'un widget parent
    .bind() lie un événement (ici clic gauche) à une fonction
    """
    btn = tk.Frame(parent, width=wid, height=hei, bd=2, relief='raised')
    btn.place(relx=0.5, rely= relly, anchor='center')
    btn.pack_propagate(False)

    for line in text_lines:
        if text_lines[1] == line:
            tk.Label(btn, text=line, font=('Helvetica', size1, boldd)).pack()
        else:
            tk.Label(btn, text=line, font=('Helvetica', size2)).pack()

    if command:
        def _on_click(event, cmd=command):
            """
            event: événement (ex. clic gauche)
            cmd: fonction à appeler
            _on_click c'est si on clique sur le bouton 
            """
            cmd()
        
        for w in btn.winfo_children():
            w.bind('<Button-1>', _on_click)
        btn.bind('<Button-1>', _on_click)

    btn.pack(fill='x', padx=10, pady=10)  # Faire en sorte que le bouton prenne toute la largeur

    return btn



# BARRE DE MENU
def create_menu(fenetre):

    def alert():
        showinfo("Alerte", "Bravo!")

    def reglesjeu():
        showinfo(
            "Règles du jeu",
            "Chaque joueur place ses navires sur une grille.\n"
            "À tour de rôle, ils tirent sur la grille adverse.\n"
            "Le but est de couler tous les navires ennemis."
        )

    menubar = tk.Menu(fenetre)


    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label="Règles du jeu", command=reglesjeu)
    menu1.add_command(label="À propos", command=alert)
    menubar.add_cascade(label="Help", menu=menu1)

    fenetre.config(menu=menubar)



# PANNEAUX
def panel(p, wid, hei, bg_color, content):
    panel = tk.Frame(p, width=wid, height=hei, background=bg_color)
    panel.pack_propagate(False)
    tk.Label(panel, text=content, background=bg_color).pack(expand=True)
    return panel

def appliquer_theme(theme, root, f1, f2, f3, boutons):
    global theme_actuel
    theme_actuel = theme

    # pour la fenêtre
    root.configure(bg=theme["bg"])

    # pour les frames
    f1.configure(bg=theme["frame"])
    f2.configure(bg=theme["frame"])
    f3.configure(bg=theme["frame"])

    # pour la grille boutons 
    for ligne in boutons:
        for b in ligne:
            b.config(bg=theme["grid"])

#pour tester le clic sur une case du grillage
def clic_case(ligne, colonne):
    print(ligne, colonne)
