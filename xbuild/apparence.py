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
    "bg": "#1a1a2e",
    "frame": "#16213e",
    "button": "#0f3460",
    "text": "#e8e8e8",
    "grid": "#533483",
    "boat": "#e94560",
    "hover": "#1a5c8a" 
}

THEME_SOMBRE = {
    "bg": "#0d1117",
    "frame": "#161b22",
    "button": "#21262d",
    "text": "#c9d1d9",
    "grid": "#30363d",
    "boat": "#58a6ff",
    "hover": "#388bfd"
}

THEME_CLASSIQUE = {
    "bg": "#f0f0f0",
    "frame": "#ffffff",
    "button": "#e0e0e0",
    "text": "#000000",
    "grid": "#b0c4de",
    "boat": "#4682b4",
    "hover": "#5a9bd4"
}

THEME_ROSE = {
    "bg": "#ffe4e1",
    "frame": "#fff0f5",
    "button": "#ffb6c1",
    "text": "#8b0000",
    "grid": "#ffc0cb",
    "boat": "#ff69b4",
    "hover": "#ff85c1"
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
        refresh_mini_grille(boutons_pvp, jeu.grille_joueur(1), theme)
    if boutons_ia:
        refresh_mini_grille(boutons_ia, jeu.grille_joueur(2), theme)

def refresh_grille(boutons, grille, theme):
    """
    Met à jour les couleurs d'une grille de boutons en fonction de l'état de jeu.
    
    Args:
        boutons: Grille de boutons Tkinter
        grille: Grille logique du jeu
        theme: Thème actif
    """
    import jeu
    
    for i in range(10):
        for j in range(10):
            case = grille[i][j]
            
            if case == jeu.BATEAU:
                boutons[i][j].config(bg=theme["boat"])
            elif case == jeu.TOUCHE:
                boutons[i][j].config(bg="red", text="X")
            elif case == jeu.RATE:
                boutons[i][j].config(bg="black", text="O")
            elif case == jeu.COULE:
                boutons[i][j].config(bg="darkred", text="⚓")
            else:  # VIDE
                boutons[i][j].config(bg=theme["grid"], text="")

def refresh_mini_grille(mini_grille, grille, theme):
    """
    Met à jour la mini-grille affichant l'état du joueur.
    """
    import jeu

    for i in range(10):
        for j in range(10):
            case = grille[i][j]

            if case == jeu.BATEAU:
                mini_grille[i][j].config(bg=theme["boat"])
            elif case == jeu.TOUCHE:
                mini_grille[i][j].config(bg="red")
            elif case == jeu.RATE:
                mini_grille[i][j].config(bg="black")
            elif case == jeu.COULE:
                mini_grille[i][j].config(bg="white")
            else:  # VIDE
                mini_grille[i][j].config(bg=theme["grid"])

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

# ==================== EFFETS DE SURVOL ====================

def ajouter_effet_survol(widget, theme):
    """
    Ajoute un effet de survol à un widget (bouton, case, etc.).
    Change la couleur et le curseur au survol.
    """
    couleur_normale = widget.cget("bg")
    couleur_survol = theme.get("hover", theme["button"])
    
    def on_enter(event):
        widget.config(bg=couleur_survol, cursor="hand2")
    
    def on_leave(event):
        widget.config(bg=couleur_normale, cursor="")
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def ajouter_effet_survol_grille(bouton, theme):
    """
    Ajoute un effet de survol spécifique pour les cases de grille.
    Ne change la couleur que si la case n'a pas encore été jouée.
    """
    def on_enter(event):
        if bouton['relief'] == 'raised':  # Case non jouée
            bouton.config(cursor="crosshair")
            # Légère surbrillance
            couleur_actuelle = bouton.cget("bg")
            if couleur_actuelle == theme["grid"]:
                bouton.config(bg=theme["hover"])
    
    def on_leave(event):
        if bouton['relief'] == 'raised':
            bouton.config(cursor="")
            couleur_actuelle = bouton.cget("bg")
            if couleur_actuelle == theme["hover"]:
                bouton.config(bg=theme["grid"])
    
    bouton.bind("<Enter>", on_enter)
    bouton.bind("<Leave>", on_leave)