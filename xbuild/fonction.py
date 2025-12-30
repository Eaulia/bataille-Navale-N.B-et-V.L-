import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
import jeu

#askstring c pour dmd qlq chose, ici l'orientation du bateau

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
def panel(p, wid, hei, theme, content):
    panel = tk.Frame(p, width=wid, height=hei, bg=theme["frame"])
    panel.pack_propagate(False)
    tk.Label(panel, text=content, bg=theme["frame"], fg=theme["text"]).pack(expand=True)
    return panel

def appliquer_theme(theme, root, frames, boutons):
    # pour la fenêtre
    root.configure(bg=theme["bg"])

    # pour les frames + widgets
    for frame in frames:
        frame.configure(bg=theme["frame"])

        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=theme["frame"], fg=theme["text"])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=theme["button"], fg=theme["text"])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=theme["button"])

            # pourrecolorer  à l'intérieur des boutons
                for sub in widget.winfo_children():
                    if isinstance(sub, tk.Label):
                        sub.configure(
                            bg=theme["button"],
                            fg=theme["text"])

            #et pr recolorer les boutons de la grille
            refresh_grille(boutons, jeu.grille_joueur1, theme_actuel)
                        



#en parcourant la grille, on met à jour les couleurs des boutons en fonction de l'état de la grille
def refresh_grille(boutons, grille, theme): 
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            etat = grille[i][j]
            if etat == jeu.BATEAU:
                boutons[i][j].configure(bg="white")
            else:
                boutons[i][j].configure(bg=theme["grid"])
                


#quand on clique dans la grille pour placer le bateau d'un joueur
def clic_placement_bateau(ligne, colonne, boutons):

    # demander quel bateau et orientation
    nom_bateau, horizontal = demander_bateau_et_orientation()
    if nom_bateau is None:
        return  # annulation
    taille = jeu.taille_bateau(nom_bateau) # obtenir la taille du bateau avc le nom


    taille = jeu.bateau_en_cours_taille()
    if taille is None:
        print("Tous les bateaux sont déjà placés.")
        return # on vérifie si tous les bateaux sont pas déjà placés

    # colorier les cases du bateau
    ok = jeu.placer_bateau(jeu.grille_joueur1, ligne, colonne, taille, horizontal)
    if ok:
        if horizontal:
            for i in range(taille):
                fn.refresh_grille(boutons, jeu.grille_joueur1, theme_actuel)


        else:
            for i in range(taille):
                boutons[ligne+i][colonne].configure(bg="white")
        jeu.indice_bateau += 1 # passer au bateau suivant
        
        if jeu.indice_bateau < len(jeu.liste_bateaux):
            showinfo("Placement suivant",
                     f"Place le bateau de taille {jeu.liste_bateaux[jeu.indice_bateau]}") # message pr prochain bateau
        else:
            showinfo("Placement terminé", "Tous les bateaux sont placés !")
    else:
        showinfo("Placement impossible", "Impossible à cet endroit.")


#petite fenêtre pour demander quel bateau et orientation, c plus clair

def demander_bateau_et_orientation():
    
    # création d’une fenêtre
    win = tk.Toplevel()
    win.title("Choisir bateau & orientation")

    # liste de bateaux disponibles (clés de BATEAUX_PRESET)
    noms_bateaux = list(jeu.BATEAUX_PRESET.keys())

    # variable pour le spinbox
    var_bateau = tk.StringVar(win)
    var_bateau.set(noms_bateaux[0])  # valeur initiale

    # variable orientation
    var_orient = tk.StringVar(win)
    var_orient.set("H")  # par défaut

    # spinbox pour choisir le bateau
    tk.Label(win, text="Choisir bateau :").pack(padx=10, pady=5)
    spin = tk.Spinbox(win, values=noms_bateaux, textvariable=var_bateau)
    spin.pack(padx=10, pady=5)

    # boutons pour choisir orientation
    frame_or = tk.Frame(win)
    tk.Label(frame_or, text="Orientation :").pack(side="left")
    tk.Radiobutton(frame_or, text="Horizontal", variable=var_orient, value="H").pack(side="left")
    tk.Radiobutton(frame_or, text="Vertical", variable=var_orient, value="V").pack(side="left")
    frame_or.pack(padx=10, pady=5)

    # valeur de retour
    result = {"bateau": None, "horiz": None}

    def valider():
        result["bateau"] = var_bateau.get()
        result["horiz"] = (var_orient.get() == "H")
        win.destroy()

    # bouton OK
    tk.Button(win, text="OK", command=valider).pack(pady=10)

    # attendre que la fenêtre soit fermée
    win.grab_set()
    win.wait_window()

    return result["bateau"], result["horiz"]
