import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
import jeu
from tkinter import messagebox

#askstring c pour dmd qlq chose, ici l'orientation du bateau
COULEUR_FOND = "#FFFFFF"  # couleur par défaut des cases vides


joueur_en_placement = 1


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

def appliquer_theme(theme, root, frames, boutons_pvp, boutons_ia):
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

            # pour recolorer  à l'intérieur des boutons
                for sub in widget.winfo_children():
                    if isinstance(sub, tk.Label):
                        sub.configure(
                            bg=theme["button"],
                            fg=theme["text"])

    # rafraîchir les grilles
    refresh_grille(boutons_pvp, jeu.grille_joueur(1), theme)
    refresh_grille(boutons_ia, jeu.grille_joueur(2), theme)



#en parcourant la grille, on met à jour les couleurs des boutons en fonction de l'état de la grille
def refresh_grille(boutons, grille, theme): 
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            etat = grille[i][j]
            if etat == jeu.BATEAU:
                boutons[i][j].configure(bg=theme["boat"])
            else:
                boutons[i][j].configure(bg=theme["grid"])
                

# placement aléatoire des bateaux 
def placement_aleatoire_interface(boutons, theme_actuel):
    jeu.placement_aleatoire(jeu.joueur_actuel)
    refresh_grille(boutons, jeu.grille_joueur(jeu.joueur_actuel), theme_actuel) #mettre à jour
    if jeu.joueur_actuel == 1:
        jeu.changer_tour()  #passer au joueur 2
        vider_grille(boutons, theme_actuel)
        messagebox.showinfo("Joueur 2", "Joueur 2 : place tes bateaux")
    else:
        # sinon, les deux joueurs ont placé leurs bateaux
        demarrer_phase_tir()



# demander quel bateau et orientation
def clic_placement_bateau(ligne, colonne, boutons, theme_actuel):

    #demander le bateau et l'orientation
    nom_bateau, horizontal = demander_bateau_et_orientation()
    if nom_bateau is None:
        return  # annulation ou plus de bateaux

    #récupérer la taille du bateau
    taille = jeu.taille_bateau(nom_bateau)
    if taille is None:
        print("Tous les bateaux sont déjà placés.")
        return

    #essayer de placer le bateau (logique du jeu)
    placement_reussi = jeu.placer_bateau(
        joueur_en_placement, nom_bateau, ligne, colonne, horizontal
    )

    if not placement_reussi:
        messagebox.showwarning(
            "Placement impossible",
            "Le bateau ne peut pas être placé ici."
        )
        return

    #affichage du bateau sur la grille 
    for i in range(taille):
        l = ligne + (0 if horizontal else i)
        c = colonne + (i if horizontal else 0)
        boutons[l][c].config(bg=theme_actuel["boat"])

    # mettre à jour la grille visuellement
    refresh_grille(boutons, jeu.grille_joueur(joueur_en_placement), theme_actuel)

    # si plus de bateaux à placer
    if not jeu.bateaux_restants_joueur(joueur_en_placement):
         if joueur_en_placement == 1:  # passer au joueur 2
             joueur_en_placement = 2
             vider_grille(boutons)
             messagebox.showinfo("Joueur 2", "Joueur 2 : place tes bateaux")
         else:  # si Joueur 2 a fini, on peut commencer la phase de tir
             demarrer_phase_tir()



def clic_placement_bateau_ia(ligne, colonne, boutons, theme_actuel):
    joueur = 1  # toujours le joueur humain

    nom_bateau, horizontal = demander_bateau_et_orientation()
    if nom_bateau is None:
        return

    taille = jeu.taille_bateau(nom_bateau)
    if taille is None:
        return

    placement_reussi = jeu.placer_bateau(
        joueur, nom_bateau, ligne, colonne, horizontal
    )

    if not placement_reussi:
        messagebox.showwarning(
            "Placement impossible",
            "Le bateau ne peut pas être placé ici."
        )
        return

    refresh_grille(boutons, jeu.grille_joueur(joueur), theme_actuel)

    # Si le joueur a fini de placer ses bateaux
    if not jeu.bateaux_restants_joueur(joueur):
        messagebox.showinfo(
            "IA",
            "L'IA place ses bateaux."
        )
        jeu.placement_aleatoire(2)
        demarrer_phase_tir()




# démarrer la phase de tir
def demarrer_phase_tir():
    messagebox.showinfo("Phase de tir", "Tous les bateaux sont placés ! Début de la bataille.")


# vider la grille des boutons
def vider_grille(boutons, theme_actuel):
    for ligne in boutons:
        for bouton in ligne:
            bouton.config(bg=theme_actuel["grid"])

#petite fenêtre pour demander quel bateau et orientation, c plus clair

def demander_bateau_et_orientation():
    # utiliser la liste des bateaux du joueur actuel
    noms_bateaux = jeu.bateaux_restants_joueur(jeu.joueur_actuel)
    
    if not noms_bateaux:
        return None, None  # plus de bateaux à placer

    # création d’une fenêtre
    win = tk.Toplevel()
    win.title("Choisir bateau & orientation")

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

def start_pvp(root, f4, f2): # Lance le mode Joueur contre Joueur

    global joueur_en_placement
    joueur_en_placement = 1

    swap_frames(f4, f2)

    root.after(
        100,
        lambda: messagebox.showinfo(
            "Placement des bateaux",
            "Joueur 1 : place tes bateaux en cliquant sur les cases."
        )
    )


def start_ia(root, f4, f5): # Lance le mode Joueur contre IA
    # on réinitialise le jeu
    jeu.reset_jeu()

    swap_frames(f4, f5)

    root.after(
        100,
        lambda: messagebox.showinfo(
            "Placement des bateaux",
            "Joueur 1 : place tes bateaux en cliquant sur les cases."
        )
    )
