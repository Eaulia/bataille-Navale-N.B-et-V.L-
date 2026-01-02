"""
Module de gestion de la navigation et des frames.

Ce module contient :
- Les fonctions de navigation entre les frames
- Le démarrage des différents modes de jeu
- La gestion des références aux frames et à la fenêtre principale
"""

import tkinter as tk
from tkinter import messagebox
import jeu
import placement as plc


# ==================== VARIABLES GLOBALES ====================

# Pour la gestion des frames
root = None
f_phase_tir = None
frame_placement_pvp = None
frame_placement_ia = None


# ==================== FONCTIONS D'ACCÈS AUX VARIABLES ====================

def get_root():
    """Retourne la fenêtre principale."""
    return root


def get_f_phase_tir():
    """Retourne le frame de la phase de tir."""
    return f_phase_tir


def get_frame_placement_pvp():
    """Retourne le frame de placement PvP."""
    return frame_placement_pvp


def get_frame_placement_ia():
    """Retourne le frame de placement contre IA."""
    return frame_placement_ia


# ==================== FONCTIONS DE NAVIGATION ====================

def swap_frames(cacher, afficher):
    """
    Échange deux frames (cache l'un et affiche l'autre).
    
    Args:
        cacher: Frame à cacher
        afficher: Frame à afficher
    """
    cacher.pack_forget()  # Retire le frame de l'affichage
    afficher.pack(fill='both', expand=True)  # Affiche le nouveau frame


def start_pvp(root_window, f4, f2):
    """
    Démarre le mode Joueur contre Joueur.
    
    Args:
        root_window: Fenêtre principale Tkinter
        f4: Frame de sélection du mode
        f2: Frame de placement PvP
    """
    plc.joueur_en_placement = 1
    plc.orientation_horizontale = True
    plc.bateau_en_cours = None
    plc.mode_actuel = 'pvp'

    # Réinitialiser le jeu avant de commencer
    jeu.reset_jeu()

    swap_frames(f4, f2)

    # Afficher le message après un court délai
    root_window.after(
        100,
        lambda: messagebox.showinfo(
            "Placement des bateaux",
            "Joueur 1 : sélectionnez un bateau puis cliquez sur la grille pour le placer.\nAppuyez sur R pour changer l'orientation."
        )
    )


def start_ia(root_window, f4, f5):
    """
    Démarre le mode Joueur contre IA.
    
    Args:
        root_window: Fenêtre principale Tkinter
        f4: Frame de sélection du mode
        f5: Frame de placement contre IA
    """
    plc.joueur_en_placement = 1
    plc.orientation_horizontale = True
    plc.bateau_en_cours = None
    plc.mode_actuel = 'ia'
    
    # Réinitialiser le jeu
    jeu.reset_jeu()

    swap_frames(f4, f5)

    # Afficher le message après un court délai
    root_window.after(
        100,
        lambda: messagebox.showinfo(
            "Placement des bateaux",
            "Joueur 1 : sélectionnez un bateau puis cliquez sur la grille pour le placer.\nAppuyez sur R pour changer l'orientation."
        )
    )
