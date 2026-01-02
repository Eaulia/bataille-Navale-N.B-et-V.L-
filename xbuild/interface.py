"""
Module de gestion de l'interface graphique.

Ce module contient :
- Les fonctions de création d'interface (boutons, menus, panneaux)
- Les effets visuels (survol, etc.)
"""

import tkinter as tk
from tkinter.messagebox import showinfo


# ==================== CONSTANTES ====================

COULEUR_FOND = "#FFFFFF"  # Couleur par défaut des cases vides


# ==================== FONCTIONS D'EFFETS VISUELS ====================

def on_enter(event, couleur_actuelle="#E0E0E0"):
    """
    Change la couleur d'une case au survol de la souris
    
    Args:
        event: Événement Tkinter
        couleur_actuelle: Couleur de survol
    """
    if event.widget['relief'] == 'raised':  # Seulement si la case est encore jouable
        event.widget['bg'] = couleur_actuelle


def on_leave(event, couleur_originale):
    """
    Restaure la couleur d'origine quand la souris part de la case
    
    Args:
        event: Événement Tkinter
        couleur_originale: Couleur à restaurer
    """
    if event.widget['relief'] == 'raised':
        event.widget['bg'] = couleur_originale


# ==================== FONCTIONS DE CRÉATION D'INTERFACE ==================== 

def creer_bouton(parent, lignes_texte, largeur, hauteur, taille_principale, 
                 taille_secondaire, style_gras, position_y, commande=None):
    """
    Crée un bouton personnalisé avec texte multi-lignes.
    
    Args:
        parent: Widget parent
        lignes_texte: Liste de lignes de texte à afficher
        largeur: Largeur du bouton
        hauteur: Hauteur du bouton
        taille_principale: Taille de la police du texte principal
        taille_secondaire: Taille de la police du texte secondaire
        style_gras: Style de police ('bold' ou '')
        position_y: Position verticale relative (0.0 à 1.0)
        commande: Fonction à exécuter au clic
    
    Returns:
        Le widget Frame du bouton
    """
    btn = tk.Frame(parent, width=largeur, height=hauteur, bd=2, relief='raised')
    btn.place(relx=0.5, rely=position_y, anchor='center')
    btn.pack_propagate(False)

    # Créer les labels pour chaque ligne de texte
    for ligne in lignes_texte:
        if lignes_texte[1] == ligne:  # Ligne principale (deuxième ligne)
            tk.Label(btn, text=ligne, font=('Helvetica', taille_principale, style_gras)).pack()
        else:  # Lignes secondaires
            tk.Label(btn, text=ligne, font=('Helvetica', taille_secondaire)).pack()

    # Lier la commande au clic
    if commande:
        def _executer_au_clic(event, cmd=commande):
            """Exécute la commande au clic."""
            cmd()
        
        # Appliquer le clic à tous les enfants du bouton
        for widget in btn.winfo_children():
            widget.bind('<Button-1>', _executer_au_clic)
        btn.bind('<Button-1>', _executer_au_clic)

    btn.pack(fill='x', padx=10, pady=10)  # Faire en sorte que le bouton prenne toute la largeur

    return btn


# Alias pour compatibilité
bouton = creer_bouton


def creer_menu(fenetre):
    """
    Crée la barre de menu de l'application.
    
    Args:
        fenetre: Fenêtre principale Tkinter
    """
    def afficher_alerte():
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
    menu1.add_command(label="À propos", command=afficher_alerte)
    menubar.add_cascade(label="Help", menu=menu1)

    fenetre.config(menu=menubar)


# Alias pour compatibilité
create_menu = creer_menu


def creer_panneau(parent, largeur, hauteur, theme, contenu):
    """
    Crée un panneau avec un label centré.
    
    Args:
        parent: Widget parent
        largeur: Largeur du panneau
        hauteur: Hauteur du panneau
        theme: Dictionnaire de thème
        contenu: Texte à afficher
    
    Returns:
        Le widget Frame du panneau
    """
    panneau = tk.Frame(parent, width=largeur, height=hauteur, bg=theme["frame"])
    panneau.pack_propagate(False)
    tk.Label(panneau, text=contenu, bg=theme["frame"], fg=theme["text"]).pack(expand=True)
    return panneau


# Alias pour compatibilité
panel = creer_panneau


def refresh_mini_grille(mini_grille, grille, theme):
    """
    Met à jour la mini-grille affichant les bateaux du joueur.
    
    Args:
        mini_grille: Grille miniature de labels Tkinter
        grille: Grille de jeu logique
        theme: Thème actif
    """
    import jeu
    
    for i in range(10):
        for j in range(10):
            if grille[i][j] == jeu.BATEAU:
                mini_grille[i][j].config(bg=theme["boat"])
            else:
                mini_grille[i][j].config(bg=theme["grid"])
