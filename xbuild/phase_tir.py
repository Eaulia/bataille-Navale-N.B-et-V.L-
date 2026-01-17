"""
Module de gestion de la phase de tir.

Ce module contient :
- L'initialisation de l'interface de tir
- La gestion des tirs et de leurs résultats
- La mise à jour des grilles pendant le jeu
"""

import tkinter as tk
from tkinter import messagebox
import jeu
import apparence as app
from interface import on_enter, on_leave, refresh_mini_grille
import random
import navigation as nav


# ==================== VARIABLES GLOBALES ====================

# Pour la gestion des frames
f_phase_tir = None

# Mémoire de l'IA
ia_cibles = []  # cases à tester après un tir touché
ia_touches = []  # cases touchées (non coulées) pour détecter le sens
ia_direction = None  # 'H' pour horizontal, 'V' pour vertical, None si sens non détecté

# ==================== FONCTIONS DE PHASE DE TIR ====================

def initialiser_phase_tir(frame, theme):
    """
    Initialise l'interface de la phase de tir.
    
    Args:
        frame: Frame conteneur
        theme: Thème actif
    """
    # Nettoyer le frame pour éviter les widgets empilés
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Créer les deux panneaux (grille joueur + grille de tir)
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
    
    # Initialiser la mini-grille avec les bateaux du joueur 1
    refresh_mini_grille(mini_grille_joueur, jeu.grilles[1], theme)

    # Grille de tir
    boutons_tir = []
    for i in range(10):
        ligne = []
        for j in range(10):
            b = tk.Label(panel_tir, width=4, height=2, bg=theme["grid"], relief="raised", borderwidth=2)
            b.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
            b.bind("<Button-1>", lambda e, l=i, c=j: clic_tir(l, c, boutons_tir, mini_grille_joueur, panel_tir))
            b.bind("<Enter>", lambda e: on_enter(e, "#D0E8E8"))
            b.bind("<Leave>", lambda e, couleur=theme["grid"]: on_leave(e, couleur))
            ligne.append(b)
        boutons_tir.append(ligne)

    # Configurer colonnes/lignes pour qu'elles prennent tout l'espace
    for i in range(10):
        panel_tir.grid_columnconfigure(i, weight=1)
        panel_tir.grid_rowconfigure(i, weight=1)

    #bouton retour 
    zone_boutons = tk.Frame(panel_tir, bg=theme["frame"])
    zone_boutons.grid(row=10, column=0, columnspan=10, pady=10)

    def retour_menu():
        jeu.reset_session()
        app.swap_frames(f_phase_tir, nav.root.children['!frame4'])

    tk.Button(
        zone_boutons,
        text="Retour au menu",
        command=retour_menu
        ).pack()

def clic_tir(ligne, colonne, boutons_tir, mini_grille_joueur, panel_tir):
    """
    Gère le clic sur une case pour tirer et affiche le résultat.
    
    Args:
        ligne: Ligne de la case ciblée (0-9)
        colonne: Colonne de la case ciblée (0-9)
        boutons_tir: Grille de boutons de tir
        mini_grille_joueur: Mini-grille affichant les bateaux du joueur
        panel_tir: Panneau contenant la grille de tir
    """
    # seul le joueur 1 peut tirer 
    if jeu.joueur_actuel != 1:
        return 

    joueur = jeu.joueur_actuel
    adversaire =2
    
    # Vérifier l'état actuel pour éviter de tirer deux fois
    etat = jeu.grilles[adversaire][ligne][colonne]
    if etat in [jeu.TOUCHE, jeu.RATE, jeu.COULE]:
        messagebox.showinfo("Info", "Case déjà ciblée !")
        return

    # Tir logique
    if etat == jeu.BATEAU:
        # touché
        jeu.grilles[adversaire][ligne][colonne] = jeu.TOUCHE
        boutons_tir[ligne][colonne].config(bg="#C83333", relief="sunken")  # rouge pour tocado

        # Vérifier si le navire est coulé
        if jeu.bateau_coule(adversaire, ligne, colonne):
            coords = jeu.coord_bateau(adversaire, ligne, colonne)  # liste des cases du bateau
            for l, c in coords:
                boutons_tir[l][c].config(bg="white", relief="sunken")  # blanc pour bateau coulé
                jeu.grilles[adversaire][l][c] = jeu.COULE
            messagebox.showinfo("Navire coulé !", "Vous avez coulé un navire !")
            
        # Vérifier la victoire
            if jeu.verifier_victoire(adversaire):
                # Incrémenter le score
                jeu.victoires_joueur1 += 1

                choix = messagebox.askquestion(
                    "Victoire !",
                    f"Le joueur {joueur} a gagné la partie !\n\n"
                    f"Score :\n"
                    f"Joueur 1 : {jeu.victoires_joueur1}\n"
                    f"Ia : {jeu.victoires_joueur2}\n\n"
                    "Rejouer ?"
                )

                from navigation import swap_frames, get_frame_placement_ia

                if choix == "yes":
                    jeu.reset_jeu()
                    swap_frames(f_phase_tir, get_frame_placement_ia())
                else:
                    jeu.reset_session()
                    swap_frames(f_phase_tir, nav.root.children['!frame4'])
                return

    else:
        # raté
        jeu.grilles[adversaire][ligne][colonne] = jeu.RATE
        boutons_tir[ligne][colonne].config(bg="#252121", relief="sunken")  # noir pour raté

    # Désactiver le clic pour ne pas tirer dessus à nouveau
    boutons_tir[ligne][colonne].unbind("<Button-1>")

    # Mettre à jour la mini-grille du joueur
    refresh_mini_grille(mini_grille_joueur, jeu.grilles[1], app.theme_actuel)

    # Changer de tour
    jeu.changer_tour()

    #tir automatique de l'IA seulement si c son tour 
    if jeu.joueur_actuel == 2:
        panel_tir.after(800, lambda: tir_ia(mini_grille_joueur))

def tir_ia(mini_grille_joueur):
    """
    IA :
    - si sens détecté (2+ touches alignées), tire dans cette direction
    - sinon tire autour si elle touche
    - sinon tire en quadrillage
    """
    global ia_cibles, ia_touches, ia_direction

    adversaire = 1  # joueur humain

    ligne = None
    colonne = None

    # ciblage: tirer autour d'un bateau touché
    while ia_cibles and ligne is None:
        l, c = ia_cibles.pop(0)
        if jeu.grilles[adversaire][l][c] in [jeu.VIDE, jeu.BATEAU]:
            ligne, colonne = l, c

    # recherche : quadrillage
    if ligne is None:
        cases_possibles = []

        for l in range(10):
            for c in range(10):
                if (l + c) % 2 == 0:
                    if jeu.grilles[adversaire][l][c] in [jeu.VIDE, jeu.BATEAU]:
                        cases_possibles.append((l, c))

        # sécurité si le quadrillage est vide
        if not cases_possibles:
            for l in range(10):
                for c in range(10):
                    if jeu.grilles[adversaire][l][c] in [jeu.VIDE, jeu.BATEAU]:
                        cases_possibles.append((l, c))

        ligne, colonne = random.choice(cases_possibles)

    # appliquer le tir
    if jeu.grilles[adversaire][ligne][colonne] == jeu.BATEAU:
        jeu.grilles[adversaire][ligne][colonne] = jeu.TOUCHE
        ia_touches.append((ligne, colonne))

        # Détecter le sens si on a au moins 2 touches
        if len(ia_touches) >= 2 and ia_direction is None:
            # Chercher si deux touches sont adjacentes et alignées
            for i in range(len(ia_touches) - 1):
                t1 = ia_touches[i]
                t2 = ligne, colonne
                
                # Vérifier si adjacentes verticalement (même colonne, lignes consécutives)
                if t1[1] == t2[1] and abs(t1[0] - t2[0]) == 1:
                    ia_direction = 'V'
                    # Nettoyer les cibles et ne garder que les verticales
                    ia_cibles = []
                    break
                # Vérifier si adjacentes horizontalement (même ligne, colonnes consécutives)
                elif t1[0] == t2[0] and abs(t1[1] - t2[1]) == 1:
                    ia_direction = 'H'
                    # Nettoyer les cibles et ne garder que les horizontales
                    ia_cibles = []
                    break
        
        # Ajouter les cases autour selon le sens détecté
        if ia_direction == 'H':
            # Sens horizontal: tirer à gauche et à droite (même ligne, colonnes différentes)
            # On cible toutes les touches existantes pour étendre dans les deux directions
            for touch in ia_touches:
                for dl, dc in [(0, -1), (0, 1)]:
                    nl, nc = touch[0] + dl, touch[1] + dc
                    if 0 <= nl < 10 and 0 <= nc < 10:
                        if jeu.grilles[adversaire][nl][nc] in [jeu.VIDE, jeu.BATEAU]:
                            if (nl, nc) not in ia_cibles:
                                ia_cibles.append((nl, nc))
        elif ia_direction == 'V':
            # Sens vertical: tirer en haut et en bas (même colonne, lignes différentes)
            # On cible toutes les touches existantes pour étendre dans les deux directions
            for touch in ia_touches:
                for dl, dc in [(-1, 0), (1, 0)]:
                    nl, nc = touch[0] + dl, touch[1] + dc
                    if 0 <= nl < 10 and 0 <= nc < 10:
                        if jeu.grilles[adversaire][nl][nc] in [jeu.VIDE, jeu.BATEAU]:
                            if (nl, nc) not in ia_cibles:
                                ia_cibles.append((nl, nc))
        else:
            # Pas de sens détecté: tirer dans les 4 directions autour de la dernière touche
            for dl, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nl, nc = ligne + dl, colonne + dc
                if 0 <= nl < 10 and 0 <= nc < 10:
                    if jeu.grilles[adversaire][nl][nc] in [jeu.VIDE, jeu.BATEAU]:
                        if (nl, nc) not in ia_cibles:
                            ia_cibles.append((nl, nc))
        
        # Vérifier si le bateau est coulé pour réinitialiser la mémoire
        if jeu.bateau_coule(adversaire, ligne, colonne):
            ia_touches = []
            ia_direction = None
            ia_cibles = []  # Réinitialiser les cibles car le bateau est coulé
            
            # Vérifier la victoire 
            if jeu.verifier_victoire(adversaire):
                jeu.victoires_joueur2 += 1

                choix = messagebox.askquestion(
                    "Défaite",
                    f"L'IA a gagné la partie.\n\n"
                    f"Score :\n"
                    f"Joueur : {jeu.victoires_joueur1}\n"
                    f"IA : {jeu.victoires_joueur2}\n\n"
                    "Rejouer ?"
                )

                from navigation import swap_frames, get_frame_placement_ia

                if choix == "yes":
                    jeu.reset_jeu()
                    swap_frames(f_phase_tir, get_frame_placement_ia())
                else:
                    jeu.reset_session()
                    swap_frames(f_phase_tir, nav.root.children['!frame4'])
                return
    else:
        jeu.grilles[adversaire][ligne][colonne] = jeu.RATE

    # mise à jour graphique
    refresh_mini_grille(mini_grille_joueur, jeu.grilles[adversaire], app.theme_actuel)

    # Retour au joueur humain
    jeu.changer_tour()


    
def demarrer_phase_tir(frame_placement_initial=None):
    """
    Démarre la phase de tir après le placement des bateaux.
    
    Args:
        frame_placement_initial: Frame de placement à cacher (PvP ou IA)
    """
    # Import local pour éviter les imports circulaires
    from navigation import get_f_phase_tir, get_frame_placement_pvp, get_frame_placement_ia, swap_frames
    
    global f_phase_tir
    f_phase_tir = get_f_phase_tir()
    
    # Si aucun frame n'est fourni, utiliser frame_placement_ia par défaut
    if frame_placement_initial is None:
        frame_placement_ia = get_frame_placement_ia()
        frame_placement_pvp = get_frame_placement_pvp()
        frame_placement_initial = frame_placement_ia if frame_placement_ia else frame_placement_pvp

    messagebox.showinfo("Phase de tir", "Tous les bateaux sont placés ! Début de la bataille.")

    # Initialiser l'interface de tir dans le frame f_phase_tir
    initialiser_phase_tir(f_phase_tir, app.theme_actuel)

    # Afficher le frame de tir
    swap_frames(frame_placement_initial, f_phase_tir)

