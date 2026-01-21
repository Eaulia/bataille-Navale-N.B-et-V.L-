"""
jeu.py sert à la logique de la Bataille Navale

il gère :
- Les grilles de jeu (10x10) pour chaque joueur
- Le placement et la gestion des bateaux
- Les tirs et leur résultat
- L'alternance des tours
- La détection de victoire
"""

import random


# ==================== CONSTANTES ====================

# États possibles d'une case de la grille
VIDE = 0      # Case vide (eau)
BATEAU = 1    # Case occupée par un bateau
TOUCHE = 2    # Bateau touché
RATE = 3      # Tir raté
COULE = 4     # Bateau coulé
victoires_joueur1 = 0 #pour compter les victoires des joueurs
victoires_joueur2 = 0 #idem


# Définition des bateaux disponibles (nom: taille)
TAILLES_BATEAUX = {
    "bateaudetaille_5": 5,
    "bateaudetaille_4": 4,
    "bateaudetaille_3": 3,
    "deuxiemebateaudetaille_3": 3,
    "bateaudetaille_2": 2
}


# ==================== VARIABLES GLOBALES ====================

positions_bateaux_j1 = {}
positions_bateaux_j2 = {}

# liste complète des bateaux 
LISTE_BATEAUX = list(TAILLES_BATEAUX.keys())

# listes des bateaux à placer pour chaque joueur
bateaux_restants_j1 = LISTE_BATEAUX.copy()
bateaux_restants_j2 = LISTE_BATEAUX.copy()

# Grilles de vides pour les deux joueurs
grille_joueur1 = [[VIDE] * 10 for _ in range(10)]
grille_joueur2 = [[VIDE] * 10 for _ in range(10)]

# Dictionnaire pour faciliter l'accès aux grilles
grilles = {1: grille_joueur1, 2: grille_joueur2}

# Joueur dont c'est le tour (1 ou 2)
joueur_actuel = 1

#compteur de coups, pour csv
coups_joueur = 0
coups_ia = 0


# ==================== FONCTIONS DE GESTION DES TOURS ====================

def changer_tour():
    """Alterne entre le joueur 1 et le joueur 2."""
    global joueur_actuel
    joueur_actuel = 2 if joueur_actuel == 1 else 1


# ==================== FONCTIONS D'ACCÈS AUX DONNÉES ====================

def grille_joueur(joueur):
    """Retourne la grille du joueur spécifié (1 ou 2)."""
    return grille_joueur1 if joueur == 1 else grille_joueur2


def taille_bateau(nom):
    """Retourne la taille d'un bateau à partir de son nom."""
    return TAILLES_BATEAUX.get(nom)


def bateaux_restants_joueur(joueur):
    """Retourne la liste des bateaux restants à placer pour un joueur."""
    return bateaux_restants_j1 if joueur == 1 else bateaux_restants_j2


def retirer_bateau(joueur, nom_bateau):
    """Retire un bateau de la liste des bateaux restants à placer."""
    if joueur == 1:
        bateaux_restants_j1.remove(nom_bateau)
    else:
        bateaux_restants_j2.remove(nom_bateau)

def positions_bateaux(joueur):
    """Retourne le dictionnaire des positions de bateaux du joueur"""
    return positions_bateaux_j1 if joueur == 1 else positions_bateaux_j2

# ==================== FONCTIONS DE PLACEMENT ====================

def peut_placer(grille, ligne, col, taille, horizontal=True):
    """
    Vérifie si un bateau peut être placé à la position donnée.
    
    Args:
        grille: La grille de jeu
        ligne: Ligne de départ (0-9)
        col: Colonne de départ (0-9)
        taille: Taille du bateau
        horizontal: True pour horizontal, False pour vertical
    
    Returns:
        True si le placement est possible, False sinon
    """
    if horizontal:
        # Vérifier que le bateau ne dépasse pas à droite
        if col + taille > 10:
            return False
        # Vérifier qu'ils ne se soient pas superposés
        for i in range(taille):
            if grille[ligne][col + i] == BATEAU:
                return False
    else:
        # Vérifier que le bateau ne dépasse pas en bas
        if ligne + taille > 10:
            return False
        # Vérifier qu'ils ne se soient pas superposés
        for i in range(taille):
            if grille[ligne + i][col] == BATEAU:
                return False
    return True


def placement_aleatoire(joueur):
    """
    Place tous les bateaux de manière aléatoire sur la grille d'un joueur.
    
    Args:
        joueur: Le numéro du joueur (1 ou 2)
    """
    # Vider la grille
    grille = grille_joueur(joueur)
    for i in range(10):
        for j in range(10):
            grille[i][j] = VIDE

    # Réinitialiser les bateaux restants
    if joueur == 1:
        global bateaux_restants_j1, positions_bateaux_j1
        bateaux_restants_j1 = LISTE_BATEAUX.copy()
        positions_bateaux_j1 = {}
    else:
        global bateaux_restants_j2, positions_bateaux_j2
        bateaux_restants_j2 = LISTE_BATEAUX.copy()
        positions_bateaux_j2 = {}

    # Placer chaque bateau aléatoirement
    for bateau in LISTE_BATEAUX:
        taille = taille_bateau(bateau)
        place_ok = False
        # Éviter les chevauchements
        while not place_ok: 
            horizontal = random.choice([True, False])
            ligne = random.randint(0, 9)
            col = random.randint(0, 9)
            place_ok = peut_placer(grille, ligne, col, taille, horizontal)
            if place_ok:
                placer_bateau(joueur, bateau, ligne, col, horizontal)
                
def placer_bateau(joueur, nom_bateau, ligne, col, horizontal):
    """
    Place un bateau sur la grille d'un joueur.
    
    Args:
        joueur: Numéro du joueur (1 ou 2)
        nom_bateau: Nom du bateau à placer
        ligne: Ligne de départ (0-9)
        col: Colonne de départ (0-9)
        horizontal: True pour horizontal, False pour vertical
    
    Returns:
        True si le placement a réussi, False sinon
    """
    # Vérifier que le bateau est disponible
    if nom_bateau not in bateaux_restants_joueur(joueur):
        return False

    taille = taille_bateau(nom_bateau)
    if taille is None:
        return False

    grille = grille_joueur(joueur)

    # Vérifier que le placement est possible
    if not peut_placer(grille, ligne, col, taille, horizontal):
        return False

    # Placer le bateau sur la grille
    positions = []
    if horizontal:
        for i in range(taille):
            grille[ligne][col + i] = BATEAU
            positions.append((ligne, col + i))
    else:
        for i in range(taille):
            grille[ligne + i][col] = BATEAU
            positions.append((ligne + i, col))

    dict_positions = positions_bateaux(joueur)
    dict_positions[nom_bateau] = positions

    # Retirer le bateau de la liste des bateaux disponibles
    retirer_bateau(joueur, nom_bateau)
    return True

# ==================== FONCTIONS DE RÉINITIALISATION D'1 PARTIE ====================

def reset_jeu():
    """
    Réinitialise complètement le jeu :
    - Vide les grilles des deux joueurs
    - Réinitialise les listes de bateaux
    - Remet le tour au joueur 1
    """
    global bateaux_restants_j1, bateaux_restants_j2, joueur_actuel
    global positions_bateaux_j1, positions_bateaux_j2
    
    bateaux_restants_j1 = LISTE_BATEAUX.copy()
    bateaux_restants_j2 = LISTE_BATEAUX.copy()
    positions_bateaux_j1 = {}
    positions_bateaux_j2 = {}
    joueur_actuel = 1

    # Vider toutes les cases des deux grilles
    for i in range(10):
        for j in range(10):
            grille_joueur1[i][j] = VIDE
            grille_joueur2[i][j] = VIDE


#===================== FONCTIONS DE REINITIALISATION DE SERIE DE PARTIES ====================

def reset_session(): 
    """
    Réinitialise toute la session 
    """
    global victoires_joueur1, victoires_joueur2, coups_joueur, coups_ia
    victoires_joueur1 = 0
    victoires_joueur2 = 0
    coups_joueur = 0
    coups_ia = 0
    reset_jeu()

# ==================== FONCTIONS DE DÉTECTION DE BATEAUX ====================

def trouver_bateau_par_position(joueur, ligne, colonne):
    """
    Trouve le bateau qui occupe une position donnée.
    
    Args:
        joueur: Numéro du joueur (1 ou 2)
        ligne: Ligne de la case (0-9)
        colonne: Colonne de la case (0-9)
    
    Returns:
        (nom_bateau, liste_positions) ou (None, None)
    """

    dict_positions = positions_bateaux(joueur)
    
    for nom_bateau, positions in dict_positions.items():
        if (ligne, colonne) in positions:
            return nom_bateau, positions
    
    return None, None


def bateau_coule(joueur, ligne, colonne):
    """
    Vérifie si le bateau à cette position est coulé.
    Args:
        joueur: Numéro du joueur (1 ou 2)
        ligne: Ligne d'une case du bateau (0-9)
        colonne: Colonne d'une case du bateau (0-9)
    
    Returns:
        True si toutes les cases du bateau sont touchées, False sinon
    """
    grille = grille_joueur(joueur)
    nom_bateau, positions = trouver_bateau_par_position(joueur, ligne, colonne)
    
    if positions is None:
        return False
    
    # Vérifier si toutes les positions du bateau sont touchées
    return all(grille[l][c] == TOUCHE for l, c in positions)


def coord_bateau(joueur, ligne, colonne):
    """Retourne les coordonnées du bateau à cette position"""
    return trouver_bateau_par_position(joueur, ligne, colonne)

""'''def trouver_bateau(joueur, ligne, colonne):
    """
    Trouve toutes les coordonnées d'un bateau à partir d'une de ses cases.
    
    Args:
        joueur: Numéro du joueur (1 ou 2)
        ligne: Ligne de la case (0-9)
        colonne: Colonne de la case (0-9)
    
    Returns:
        Liste des coordonnées (ligne, colonne) du bateau, ou None si pas de bateau
    """
    grille = grille_joueur(joueur)
    
    # Vérifier qu'il y a un bateau à cette position
    if grille[ligne][colonne] not in (BATEAU, TOUCHE):
        return None

    # Recherche horizontale
    start_col = colonne
    while start_col > 0 and grille[ligne][start_col - 1] in (BATEAU, TOUCHE):
        start_col -= 1
    end_col = colonne
    while end_col < 9 and grille[ligne][end_col + 1] in (BATEAU, TOUCHE):
        end_col += 1
    if end_col - start_col + 1 > 1:
        return [(ligne, c) for c in range(start_col, end_col + 1)]

    # Recherche verticale
    start_row = ligne
    while start_row > 0 and grille[start_row - 1][colonne] in (BATEAU, TOUCHE):
        start_row -= 1
    end_row = ligne
    while end_row < 9 and grille[end_row + 1][colonne] in (BATEAU, TOUCHE):
        end_row += 1
    if end_row - start_row + 1 > 1:
        return [(r, colonne) for r in range(start_row, end_row + 1)]

    # Bateau de taille 1
    return [(ligne, colonne)]


def bateau_coule(joueur, ligne, colonne):
    """
    Vérifie si un bateau est coulé.
    
    Args:
        joueur: Numéro du joueur (1 ou 2)
        ligne: Ligne d'une case du bateau (0-9)
        colonne: Colonne d'une case du bateau (0-9)
    
    Returns:
        True si toutes les cases du bateau sont touchées, False sinon
    """
    bateau = trouver_bateau(joueur, ligne, colonne)
    if bateau is None:
        return False
    return all(grilles[joueur][l][c] == TOUCHE for l, c in bateau)


def coord_bateau(joueur, ligne, colonne):
    """Retourne les coordonnées d'un bateau."""
    return trouver_bateau(joueur, ligne, colonne)'''""


# ==================== FONCTIONS DE VICTOIRE ====================

def verifier_victoire(joueur):
    """
    Vérifie si tous les bateaux d'un joueur ont été coulés.
    
    Args:
        joueur: Numéro du joueur à vérifier (1 ou 2)
    
    Returns:
        True si tous les bateaux sont coulés (= défaite), False sinon
    """
    for ligne in grilles[joueur]:
        for case in ligne:
            if case == BATEAU:
                return False
    return True
