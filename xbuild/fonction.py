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
    global joueur_en_placement  # Pour mettre à jour le joueur qui place

    jeu.placement_aleatoire(jeu.joueur_actuel)
    refresh_grille(boutons, jeu.grille_joueur(jeu.joueur_actuel), theme_actuel)

    if jeu.joueur_actuel == 1:
        jeu.changer_tour()  # Passe au joueur 2
        joueur_en_placement = jeu.joueur_actuel  # Mettre à jour le joueur en placement
        vider_grille(boutons, theme_actuel)  # Vide la grille pour joueur 2
        messagebox.showinfo("Joueur 2", "Joueur 2 : place tes bateaux")
    else:
        demarrer_phase_tir()




# placement aléatoire des bateaux pour l'IA
def placement_aleatoire_interface_ia(boutons, theme_actuel, mini_grille_joueur):
    joueur = 1  # joueur humain
    
    # Placer aléatoirement bateaux joueur humain
    jeu.placement_aleatoire(joueur)
    refresh_grille(boutons, jeu.grille_joueur(joueur), theme_actuel)
    
    # Placer aléatoirement bateaux IA
    jeu.placement_aleatoire(2)  # IA = joueur 2
    
    # Mettre à jour la mini-grille du joueur humain (affichage)
    refresh_mini_grille(mini_grille_joueur, jeu.grille_joueur(joueur), theme_actuel)
    
    # Démarrer la phase de tir
    demarrer_phase_tir()





# gestion du clic sur une case pour placer un bateau
def clic_placement_bateau(ligne, colonne, boutons, theme_actuel):
    global joueur_en_placement  # joueur qui place ses bateaux

    #demander quel bateau et orientation
    nom_bateau, horizontal = demander_bateau_et_orientation(joueur_en_placement)
    if nom_bateau is None:
        return  # annulation ou plus de bateaux

    #vérifier que le bateau est encore disponible
    if nom_bateau not in jeu.bateaux_restants_joueur(joueur_en_placement):
        messagebox.showinfo("Info", "Ce bateau a déjà été placé !")
        return

    # récupérer la taille
    taille = jeu.taille_bateau(nom_bateau)
    if taille is None:
        messagebox.showwarning("Erreur", "Impossible de récupérer la taille du bateau.")
        return

    #essayer de placer le bateau
    placement_reussi = jeu.placer_bateau(
        joueur_en_placement, nom_bateau, ligne, colonne, horizontal
    )

    if not placement_reussi:
        messagebox.showwarning("Placement impossible", "Le bateau ne peut pas être placé ici.")
        return

    #afficher le bateau sur la grille
    for i in range(taille):
        l = ligne + (0 if horizontal else i)
        c = colonne + (i if horizontal else 0)
        boutons[l][c].config(bg=theme_actuel["boat"])

    #mettre à jour la grille visuellement
    refresh_grille(boutons, jeu.grille_joueur(joueur_en_placement), theme_actuel)

    #vérifier si le joueur a terminé tous ses bateaux
    if not jeu.bateaux_restants_joueur(joueur_en_placement):
        if joueur_en_placement == 1:
            # passer au joueur 2
            joueur_en_placement = 2
            vider_grille(boutons, theme_actuel)
            messagebox.showinfo("Joueur 2", "Joueur 2 : place tes bateaux")
        else:
            # tous les joueurs ont placé leurs bateaux
            demarrer_phase_tir()


# gestion du clic sur une case pour placer un bateau contre l'IA
def clic_placement_bateau_ia(ligne, colonne, boutons, theme_actuel, paned, panel1, mini_grille_joueur):
    joueur = 1  # toujours le joueur humain

    # demander quel bateau et orientation
    nom_bateau, horizontal = demander_bateau_et_orientation(joueur)
    if nom_bateau is None:
        return  # annulation ou plus de bateaux

    # vérifier que le bateau est encore disponible
    if nom_bateau not in jeu.bateaux_restants_joueur(joueur):
        messagebox.showinfo("Info", "Ce bateau a déjà été placé !")
        return

    # récupérer la taille
    taille = jeu.taille_bateau(nom_bateau)
    if taille is None:
        messagebox.showwarning("Erreur", "Impossible de récupérer la taille du bateau.")
        return

    # essayer de placer le bateau
    placement_reussi = jeu.placer_bateau(joueur, nom_bateau, ligne, colonne, horizontal)
    if not placement_reussi:
        messagebox.showwarning("Placement impossible", "Le bateau ne peut pas être placé ici.")
        return

    # mettre à jour la grille du joueur
    refresh_grille(boutons, jeu.grille_joueur(joueur), theme_actuel)

    # vérifier si le joueur a terminé tous ses bateaux
    if not jeu.bateaux_restants_joueur(joueur):
        # placement aléatoire des bateaux de l'IA
        jeu.placement_aleatoire(2)  # IA = joueur 2

        # ajouter la mini-grille si ce n’est pas fait
        if not panel1.winfo_ismapped():
            paned.add(panel1)

        # afficher la mini-grille du joueur
        refresh_mini_grille(mini_grille_joueur, jeu.grille_joueur(joueur), theme_actuel)

        # démarrer la phase de tir (swap automatique du frame IA → phase de tir)
        demarrer_phase_tir(frame_placement_initial=frame_placement)  




# vider la grille des boutons
def vider_grille(boutons, theme_actuel):
    for ligne in boutons:
        for bouton in ligne:
            bouton.config(bg=theme_actuel["grid"])

#petite fenêtre pour demander quel bateau et orientation, c plus clair

def demander_bateau_et_orientation(joueur):
    # utiliser la liste des bateaux du joueur actuel
    noms_bateaux = jeu.bateaux_restants_joueur(joueur)
    if not noms_bateaux:
        return None, None  # plus de bateaux à placer
    
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


# démarrer le mode Joueur contre Joueur
def start_pvp(root, f4, f2):
    global joueur_en_placement
    joueur_en_placement = 1

    # Réinitialiser le jeu avant de commencer
    jeu.reset_jeu()

    swap_frames(f4, f2)

    root.after(
        100,
        lambda: messagebox.showinfo(
            "Placement des bateaux",
            "Joueur 1 : place tes bateaux en cliquant sur les cases."
        )
    )



def start_ia(root, f4, f5): # Lance le mode Joueur contre IA
    global joueur_en_placement
    joueur_en_placement = 1
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

# réinitialiser la mini-grille affichant les bateaux du joueur 
def refresh_mini_grille(mini_grille, grille, theme):
    for i in range(10):
        for j in range(10):
            if grille[i][j] == jeu.BATEAU:
                mini_grille[i][j].config(bg=theme["boat"])
            else:
                mini_grille[i][j].config(bg=theme["grid"])



def initialiser_phase_tir(frame, theme):
    # Panels pour grille du joueur et grille de tir
    p = tk.PanedWindow(frame, orient=tk.HORIZONTAL)
    p.pack(fill='both', expand=True)

    panel_joueur = tk.Frame(p, width=120, bg=theme["frame"])
    panel_tir = tk.Frame(p, width=250, bg=theme["frame"])
    p.add(panel_joueur)
    p.add(panel_tir)

        # Grille du joueur
    mini_grille_joueur = []
    for i in range(10):
        ligne = []
        for j in range(10):
            b = tk.Label(panel_joueur, width=2, height=1, bg=theme["grid"], relief="solid", borderwidth=1)
            b.grid(row=i, column=j, padx=1, pady=1)
            ligne.append(b)
        mini_grille_joueur.append(ligne)

    # Grille de tir
    boutons_tir = []
    for i in range(10):
        ligne = []
        for j in range(10):
            b = tk.Button(panel_tir, width=2, height=1, bg=theme["grid"],
                          command=lambda l=i, c=j: clic_tir(l, c, boutons_tir, mini_grille_joueur, panel_tir))
            b.grid(row=i, column=j, sticky="nsew")
            ligne.append(b)
        boutons_tir.append(ligne)

    # Configurer colonnes/lignes pour qu'elles prennent tout l'espace
    for i in range(10):
        panel_joueur.grid_columnconfigure(i, weight=1)
        panel_joueur.grid_rowconfigure(i, weight=1)
        panel_tir.grid_columnconfigure(i, weight=1)
        panel_tir.grid_rowconfigure(i, weight=1)



# gestion du clic sur une case pour tirer et change la couleur en fonction du résultat
def clic_tir(ligne, colonne, boutons_tir, mini_grille_joueur, panel_tir):

    joueur = 1  # joueur humain
    adversaire = 2

    # Vérifier l'état actuel pour éviter de tirer deux fois
    etat = jeu.grilles[adversaire][ligne][colonne]
    if etat in [jeu.TOUCHE, jeu.RATE, jeu.COULE]:
        messagebox.showinfo("Info", "Case déjà ciblée !")
        return

    # Tir logique
    if etat == jeu.BATEAU:
        # touché
        jeu.grilles[adversaire][ligne][colonne] = jeu.TOUCHE
        boutons_tir[ligne][colonne].config(bg="black")  # noir pour touché

        # Vérifier si le navire est coulé
        if jeu.bateau_coule(adversaire, ligne, colonne):
            coords = jeu.coord_bateau(adversaire, ligne, colonne)  # liste des cases du bateau
            for l, c in coords:
                boutons_tir[l][c].config(bg="white")  # blanc pour bateau coulé
                jeu.grilles[adversaire][l][c] = jeu.COULE
            messagebox.showinfo("Navire coulé !", "Vous avez coulé un navire !")
    else:
        # raté
        jeu.grilles[adversaire][ligne][colonne] = jeu.RATE
        boutons_tir[ligne][colonne].config(bg="red")  # rouge pour raté

    # Désactiver le bouton pour ne pas tirer dessus à nouveau
    boutons_tir[ligne][colonne].config(state="disabled")

    # Mettre à jour la mini-grille du joueur
    refresh_mini_grille(mini_grille_joueur, jeu.grilles[joueur], app.theme_actuel)





# démarrer la phase de tir et passage du frame de placement à celui de tir 
def demarrer_phase_tir(frame_placement_initial):
    global f_phase_tir, root 

    messagebox.showinfo("Phase de tir", "Tous les bateaux sont placés ! Début de la bataille.")

    # Initialiser l'interface de tir dans le frame f_phase_tir
    initialiser_phase_tir(f_phase_tir, app.theme_actuel)

    # Afficher le frame de tir
    swap_frames(frame_placement_initial, f_phase_tir)




