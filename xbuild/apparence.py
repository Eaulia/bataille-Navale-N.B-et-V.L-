"""
Module de gestion de l'apparence et des thèmes de l'application.

Ce module contient :
- La définition de tous les thèmes disponibles
- Les fonctions pour appliquer et changer de thème
- Les fonctions pour rafraîchir l'affichage des grilles
"""

import tkinter as tk


# ==================== DÉFINITION DES THÈMES ====================

THEME_BLEU = {
    "bg": "#006E6E",
    "frame": "#006E6E",
    "grid": "lightblue",
    "button": "#4FA3A3",
    "text": "white",
    "boat": "white"
}

THEME_SOMBRE = {
    "bg": "#1E1E1E",
    "frame": "#1E1E1E",
    "grid": "#444444",
    "button": "#333333",
    "text": "white",
    "boat": "white"
}

THEME_CLASSIQUE = {
    "bg": "#F0F0F0",
    "frame": "#F0F0F0",
    "grid": "white",
    "button": "#E0E0E0",
    "text": "black",
    "boat": "white"
}

THEME_ROSE = {
    "bg": "#FFB6C1",
    "frame": "#FFB6C1",
    "grid": "#FFDDEE",
    "button": "#FF99AA",
    "text": "black",
    "boat": "white"
}

# Thème par défaut
theme_actuel = THEME_BLEU


# ==================== FONCTIONS DE GESTION DES THÈMES ====================

def appliquer_theme(theme, root, frames, boutons_pvp, boutons_ia):
    """
    Applique un thème à l'interface graphique.
    
    Args:
        theme: Dictionnaire contenant les couleurs du thème
        root: Fenêtre principale Tkinter
        frames: Liste des frames de l'application
        boutons_pvp: Liste des boutons de la grille PvP
        boutons_ia: Liste des boutons de la grille IA
    """
    # Import plus tard pour éviter l'import circulaire
    import jeu
    
    # Appliquer le thème à la fenêtre principale
    root.configure(bg=theme["bg"])

    # Appliquer le thème à tous les frames et leurs widgets
    for frame in frames:
        frame.configure(bg=theme["frame"])

        for widget in frame.winfo_children():
            # Appliquer aux labels
            if isinstance(widget, tk.Label):
                widget.configure(bg=theme["frame"], fg=theme["text"])
            # Appliquer aux boutons
            elif isinstance(widget, tk.Button):
                widget.configure(bg=theme["button"], fg=theme["text"])
            # Appliquer aux frames internes
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=theme["button"])
                # pour recolorer à l'intérieur des boutons
                for sub_widget in widget.winfo_children():
                    if isinstance(sub_widget, tk.Label):
                        sub_widget.configure(bg=theme["button"], fg=theme["text"])

    # rafraîchir les grilles
    if boutons_pvp:
        refresh_grille(boutons_pvp, jeu.grille_joueur(1), theme)
    if boutons_ia:
        refresh_grille(boutons_ia, jeu.grille_joueur(2), theme)

def refresh_grille(boutons, grille, theme):
    """
    Met à jour les couleurs d'une grille de boutons en fonction de l'état de jeu.
    
    Args:
        boutons: Grille de boutons Tkinter
        grille: Grille logique du jeu
        theme: Thème actif
    """
    import jeu
    
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            etat = grille[i][j]
            if etat == jeu.BATEAU:
                boutons[i][j].configure(bg=theme["boat"])
            else:
                boutons[i][j].configure(bg=theme["grid"])


def changer_theme(theme, root, frames, boutons_pvp, boutons_ia):
    """
    Change le thème de l'application.
    
    Args:
        theme: Dictionnaire contenant les couleurs du thème
        root: Fenêtre principale Tkinter
        frames: Liste des frames de l'application
        boutons_pvp: Liste des boutons de la grille PvP
        boutons_ia: Liste des boutons de la grille IA
    """
    global theme_actuel
    theme_actuel = theme
    appliquer_theme(theme_actuel, root, frames, boutons_pvp, boutons_ia)


def get_theme_actuel():
    """Retourne le thème actuellement utilisé."""
    return theme_actuel
