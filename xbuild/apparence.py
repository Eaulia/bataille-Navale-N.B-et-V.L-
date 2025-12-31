"""
Module de gestion de l'apparence et des thèmes de l'application.
"""
import fonction as fn


# ========== DÉFINITION DES THÈMES ==========
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
    fn.appliquer_theme(theme_actuel, root, frames, boutons_pvp, boutons_ia)


def get_theme_actuel():
    """Retourne le thème actuellement utilisé."""
    return theme_actuel
