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


# ==================== VARIABLES GLOBALES ====================

# Pour la gestion des frames
f_phase_tir = None


# ==================== FONCTIONS DE PHASE DE TIR ====================

def initialiser_phase_tir(frame, theme):
    """
    Initialise l'interface de la phase de tir.
    
    Args:
        frame: Frame conteneur
        theme: Thème actif
    """
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
        panel_joueur.grid_columnconfigure(i, weight=1)
        panel_joueur.grid_rowconfigure(i, weight=1)
        panel_tir.grid_columnconfigure(i, weight=1)
        panel_tir.grid_rowconfigure(i, weight=1)


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
    joueur = 1  # Joueur humain
    adversaire = 2  # IA ou joueur 2

    # Vérifier l'état actuel pour éviter de tirer deux fois
    etat = jeu.grilles[adversaire][ligne][colonne]
    if etat in [jeu.TOUCHE, jeu.RATE, jeu.COULE]:
        messagebox.showinfo("Info", "Case déjà ciblée !")
        return

    # Tir logique
    if etat == jeu.BATEAU:
        # touché
        jeu.grilles[adversaire][ligne][colonne] = jeu.TOUCHE
        boutons_tir[ligne][colonne].config(bg="black", relief="sunken")  # noir pour touché

        # Vérifier si le navire est coulé
        if jeu.bateau_coule(adversaire, ligne, colonne):
            coords = jeu.coord_bateau(adversaire, ligne, colonne)  # liste des cases du bateau
            for l, c in coords:
                boutons_tir[l][c].config(bg="white", relief="sunken")  # blanc pour bateau coulé
                jeu.grilles[adversaire][l][c] = jeu.COULE
            messagebox.showinfo("Navire coulé !", "Vous avez coulé un navire !")
    else:
        # raté
        jeu.grilles[adversaire][ligne][colonne] = jeu.RATE
        boutons_tir[ligne][colonne].config(bg="red", relief="sunken")  # rouge pour raté

    # Désactiver le clic pour ne pas tirer dessus à nouveau
    boutons_tir[ligne][colonne].unbind("<Button-1>")

    # Mettre à jour la mini-grille du joueur
    refresh_mini_grille(mini_grille_joueur, jeu.grilles[joueur], app.theme_actuel)


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
