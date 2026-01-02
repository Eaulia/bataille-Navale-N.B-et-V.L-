"""
Module de gestion du placement des bateaux.

Ce module contient :
- Les fonctions de drag and drop
- Le placement manuel et aléatoire des bateaux
- La prévisualisation et validation du placement
"""

import tkinter as tk
from tkinter import messagebox
import jeu
import apparence as app


# ==================== VARIABLES GLOBALES ====================

# Variables pour le drag and drop
bateau_en_cours = None  # Nom du bateau en cours de placement
orientation_horizontale = True  # Orientation du bateau (True = horizontal, False = vertical)
preview_cases = []  # Cases de prévisualisation
drag_widgets_pvp = {}  # Widgets de bateaux pour le mode PvP
drag_widgets_ia = {}  # Widgets de bateaux pour le mode IA
orientation_label_pvp = None  # Label d'orientation pour PvP
orientation_label_ia = None  # Label d'orientation pour IA
mode_actuel = None  # Mode de jeu actuel ('pvp' ou 'ia')

# Joueur actuellement en train de placer ses bateaux
joueur_en_placement = 1


# ==================== FONCTIONS DRAG AND DROP ====================

def creer_widget_bateau(parent, nom_bateau, taille, theme):
    """
    Crée un widget représentant un bateau pour le drag and drop.
    
    Args:
        parent: Widget parent
        nom_bateau: Nom du bateau
        taille: Taille du bateau
        theme: Thème actuel
    
    Returns:
        Le widget Frame du bateau
    """
    # Créer un frame pour le bateau
    bateau_frame = tk.Frame(parent, bg=theme["button"], relief="raised", borderwidth=2)
    
    # Afficher le nom du bateau et sa taille
    nom_court = nom_bateau.replace("bateaudetaille_", "Bateau ").replace("deuxiemebateaudetaille_", "Bateau ")
    label = tk.Label(bateau_frame, text=f"{nom_court} ({taille})", 
                    bg=theme["button"], fg=theme["text"], font=('Arial', 10, 'bold'))
    label.pack(pady=5)
    
    # Créer une représentation visuelle du bateau
    visual_frame = tk.Frame(bateau_frame, bg=theme["button"])
    visual_frame.pack(pady=5)
    
    for i in range(taille):
        case = tk.Label(visual_frame, width=3, height=1, bg=theme["boat"], 
                       relief="solid", borderwidth=1)
        case.pack(side="left", padx=1)
    
    bateau_frame.pack(pady=5, padx=10, fill="x")
    
    # Rendre le bateau cliquable pour la sélection
    def selectionner_bateau(event=None):
        global bateau_en_cours
        bateau_en_cours = nom_bateau
        # Mettre en évidence le bateau sélectionné
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(relief="raised", borderwidth=2)
        bateau_frame.config(relief="sunken", borderwidth=3)
    
    bateau_frame.bind("<Button-1>", selectionner_bateau)
    label.bind("<Button-1>", selectionner_bateau)
    
    return bateau_frame


def previsualiser_placement(ligne, col, boutons, theme):
    """
    Affiche une prévisualisation du placement du bateau.
    
    Args:
        ligne: Ligne de départ
        col: Colonne de départ
        boutons: Grille de boutons
        theme: Thème actuel
    """
    global preview_cases, bateau_en_cours, orientation_horizontale
    
    # Effacer l'ancienne prévisualisation
    effacer_previsualisation(boutons, theme)
    
    if bateau_en_cours is None:
        return
    
    taille = jeu.taille_bateau(bateau_en_cours)
    if taille is None:
        return
    
    # Vérifier si le placement est possible
    grille = jeu.grille_joueur(joueur_en_placement)
    placement_valide = jeu.peut_placer(grille, ligne, col, taille, orientation_horizontale)
    
    # Couleur de prévisualisation
    couleur = "lightgreen" if placement_valide else "#FF6666"
    
    # Afficher la prévisualisation
    for i in range(taille):
        if orientation_horizontale:
            r, c = ligne, col + i
        else:
            r, c = ligne + i, col
        
        if 0 <= r < 10 and 0 <= c < 10:
            # Vérifier que la case n'est pas déjà occupée par un bateau
            if grille[r][c] == jeu.VIDE:
                boutons[r][c].config(bg=couleur)
                preview_cases.append((r, c))


def effacer_previsualisation(boutons, theme):
    """
    Efface la prévisualisation du placement.
    
    Args:
        boutons: Grille de boutons
        theme: Thème actuel
    """
    global preview_cases
    
    grille = jeu.grille_joueur(joueur_en_placement)
    for r, c in preview_cases:
        if grille[r][c] == jeu.VIDE:
            boutons[r][c].config(bg=theme["grid"])
    
    preview_cases = []


def placer_bateau_drag(ligne, col, boutons, theme, widgets_dict):
    """
    Place le bateau sélectionné sur la grille.
    
    Args:
        ligne: Ligne de placement
        col: Colonne de placement
        boutons: Grille de boutons
        theme: Thème actuel
        widgets_dict: Dictionnaire des widgets de bateaux
    
    Returns:
        True si le placement a réussi, False sinon
    """
    global bateau_en_cours, orientation_horizontale, joueur_en_placement
    
    if bateau_en_cours is None:
        return False
    
    # Vérifier que le bateau est encore disponible
    if bateau_en_cours not in jeu.bateaux_restants_joueur(joueur_en_placement):
        messagebox.showinfo("Info", "Ce bateau a déjà été placé !")
        return False
    
    # Récupérer la taille
    taille = jeu.taille_bateau(bateau_en_cours)
    if taille is None:
        return False
    
    # Essayer de placer le bateau
    placement_reussi = jeu.placer_bateau(
        joueur_en_placement, bateau_en_cours, ligne, col, orientation_horizontale
    )
    
    if not placement_reussi:
        messagebox.showwarning("Placement impossible", "Le bateau ne peut pas être placé ici.")
        return False
    
    # Mettre à jour l'affichage
    app.refresh_grille(boutons, jeu.grille_joueur(joueur_en_placement), theme)
    
    # Supprimer le widget du bateau placé
    if bateau_en_cours in widgets_dict:
        widgets_dict[bateau_en_cours].destroy()
        del widgets_dict[bateau_en_cours]
    
    # Désélectionner le bateau
    bateau_en_cours = None
    
    return True


def basculer_orientation(orientation_label=None):
    """
    Bascule l'orientation du bateau entre horizontal et vertical.
    """
    global orientation_horizontale
    orientation_horizontale = not orientation_horizontale
    if orientation_label:
        texte_orientation = "Horizontal" if orientation_horizontale else "Vertical"
        orientation_label.config(text=f"Orientation: {texte_orientation}\n(Touche R pour pivoter)")


def rotation_touche_r():
    """
    Gère la rotation avec la touche R selon le mode actuel.
    """
    global mode_actuel, orientation_label_pvp, orientation_label_ia
    
    if mode_actuel == 'pvp' and orientation_label_pvp:
        basculer_orientation(orientation_label_pvp)
    elif mode_actuel == 'ia' and orientation_label_ia:
        basculer_orientation(orientation_label_ia)


def creer_panneau_bateaux(parent, joueur, theme):
    """
    Crée le panneau contenant les bateaux disponibles pour le drag and drop.
    
    Args:
        parent: Widget parent
        joueur: Numéro du joueur
        theme: Thème actuel
    
    Returns:
        Dictionnaire des widgets de bateaux créés et le label d'orientation
    """
    # Frame pour les instructions
    instructions = tk.Label(parent, text="Sélectionnez un bateau\net cliquez sur la grille",
                          bg=theme["frame"], fg=theme["text"], font=('Arial', 10, 'bold'))
    instructions.pack(pady=10)
    
    # Label pour l'orientation
    orientation_label = tk.Label(parent, text="Orientation: Horizontal\n(Touche R pour pivoter)",
                                bg=theme["frame"], fg=theme["text"], font=('Arial', 9))
    orientation_label.pack(pady=5)
    
    # Frame scrollable pour les bateaux
    bateaux_frame = tk.Frame(parent, bg=theme["frame"])
    bateaux_frame.pack(fill="both", expand=True, pady=10)
    
    widgets_dict = {}
    
    # Créer les widgets de bateaux
    bateaux = jeu.bateaux_restants_joueur(joueur)
    for nom_bateau in bateaux:
        taille = jeu.taille_bateau(nom_bateau)
        widget = creer_widget_bateau(bateaux_frame, nom_bateau, taille, theme)
        widgets_dict[nom_bateau] = widget
    
    return widgets_dict, orientation_label


def recreer_panneau_bateaux_pvp(theme):
    """
    Recrée le panneau de bateaux pour le joueur 2 en mode PvP.
    
    Args:
        theme: Thème actuel
    """
    global drag_widgets_pvp, orientation_label_pvp, bateau_en_cours, orientation_horizontale, joueur_en_placement
    
    # Réinitialiser
    bateau_en_cours = None
    orientation_horizontale = True
    
    # Réinitialiser les bateaux du joueur 2 dans jeu.py
    jeu.bateaux_restants_j2 = jeu.LISTE_BATEAUX.copy()
    
    # Détruire les anciens widgets
    for widget in drag_widgets_pvp.values():
        try:
            widget.destroy()
        except:
            pass
    drag_widgets_pvp.clear()
    
    # Recréer les widgets pour le joueur 2
    if orientation_label_pvp and orientation_label_pvp.winfo_exists():
        # Trouver le parent des widgets
        parent = orientation_label_pvp.master
        # Détruire tous les widgets enfants
        for widget in parent.winfo_children():
            try:
                widget.destroy()
            except:
                pass
        
        # Recréer le panneau de bateaux
        drag_widgets_pvp, orientation_label_pvp = creer_panneau_bateaux(parent, joueur_en_placement, theme)


# ==================== FONCTIONS DE PLACEMENT DES BATEAUX ==================== 

def placement_aleatoire_interface(boutons, theme_actuel):
    """
    Place aléatoirement les bateaux et met à jour l'interface (mode PvP).
    
    Args:
        boutons: Grille de boutons Tkinter
        theme_actuel: Thème actif
    """
    global joueur_en_placement

    # Placer les bateaux aléatoirement
    jeu.placement_aleatoire(jeu.joueur_actuel)
    app.refresh_grille(boutons, jeu.grille_joueur(jeu.joueur_actuel), theme_actuel)

    # Gérer la transition entre les joueurs
    if jeu.joueur_actuel == 1:
        jeu.changer_tour()  # Passe au joueur 2
        joueur_en_placement = jeu.joueur_actuel  # Mettre à jour le joueur en placement
        vider_grille(boutons, theme_actuel)  # Vide la grille pour joueur 2
        messagebox.showinfo("Joueur 2", "Joueur 2 : place tes bateaux")
    else:
        # Import local pour éviter les imports circulaires
        from phase_tir import demarrer_phase_tir
        demarrer_phase_tir()


def placement_aleatoire_interface_ia(boutons, theme_actuel, mini_grille_joueur=None):
    """
    Place aléatoirement les bateaux pour le joueur et l'IA (mode contre IA).
    
    Args:
        boutons: Grille de boutons Tkinter
        theme_actuel: Thème actif
        mini_grille_joueur: Non utilisé (conservé pour compatibilité)
    """
    joueur = 1  # Joueur humain
    
    # Placer aléatoirement bateaux joueur humain
    jeu.placement_aleatoire(joueur)
    app.refresh_grille(boutons, jeu.grille_joueur(joueur), theme_actuel)
    
    # Placer aléatoirement bateaux IA
    jeu.placement_aleatoire(2)  # IA = joueur 2
    
    # Démarrer la phase de tir
    from phase_tir import demarrer_phase_tir
    demarrer_phase_tir()


def clic_placement_bateau(ligne, colonne, boutons, theme_actuel):
    """
    Gère le clic sur une case pour placer un bateau (mode PvP - avec drag and drop).
    
    Args:
        ligne: Numéro de ligne cliquée (0-9)
        colonne: Numéro de colonne cliquée (0-9)
        boutons: Grille de boutons Tkinter
        theme_actuel: Thème actif
    """
    global joueur_en_placement, drag_widgets_pvp
    
    # Import local pour éviter les imports circulaires
    from navigation import get_root
    
    # Effacer la prévisualisation
    effacer_previsualisation(boutons, theme_actuel)
    
    # Placer le bateau sélectionné
    placement_reussi = placer_bateau_drag(ligne, colonne, boutons, theme_actuel, drag_widgets_pvp)
    
    if placement_reussi:
        # Vérifier si le joueur a terminé tous ses bateaux
        if not jeu.bateaux_restants_joueur(joueur_en_placement):
            if joueur_en_placement == 1:
                # Passer au joueur 2
                joueur_en_placement = 2
                vider_grille(boutons, theme_actuel)
                # Recréer le panneau de bateaux pour le joueur 2
                recreer_panneau_bateaux_pvp(theme_actuel)
                # Afficher le message après un court délai pour éviter le crash
                root = get_root()
                if root:
                    root.after(100, lambda: messagebox.showinfo("Joueur 2", "Joueur 2 : place tes bateaux"))
            else:
                # Tous les joueurs ont placé leurs bateaux
                from phase_tir import demarrer_phase_tir
                demarrer_phase_tir()


def clic_placement_bateau_ia(ligne, colonne, boutons, theme_actuel, paned=None, panel1=None, mini_grille_joueur=None):
    """
    Gère le clic sur une case pour placer un bateau (mode contre IA).
    
    Args:
        ligne: Numéro de ligne cliquée (0-9)
        colonne: Numéro de colonne cliquée (0-9)
        boutons: Grille de boutons Tkinter
        theme_actuel: Thème actif
        paned: Widget PanedWindow (non utilisé)
        panel1: Panneau (non utilisé)
        mini_grille_joueur: Grille miniature (non utilisé)
    """
    global drag_widgets_ia
    joueur = 1  # Toujours le joueur humain

    # Effacer la prévisualisation
    effacer_previsualisation(boutons, theme_actuel)
    
    # Placer le bateau sélectionné
    placement_reussi = placer_bateau_drag(ligne, colonne, boutons, theme_actuel, drag_widgets_ia)
    
    if placement_reussi:
        # Vérifier si le joueur a terminé tous ses bateaux
        if not jeu.bateaux_restants_joueur(joueur):
            # Placement aléatoire des bateaux de l'IA
            jeu.placement_aleatoire(2)  # IA = joueur 2

            # Démarrer la phase de tir (swap automatique du frame IA → phase de tir)
            from phase_tir import demarrer_phase_tir
            demarrer_phase_tir()


def vider_grille(boutons, theme_actuel):
    """
    Réinitialise visuellement toutes les cases de la grille.
    
    Args:
        boutons: Grille de boutons Tkinter
        theme_actuel: Thème actif
    """
    for ligne in boutons:
        for bouton in ligne:
            bouton.config(bg=theme_actuel["grid"])
