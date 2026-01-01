from random import*

# nouveau dossier après avoir fini l'interface etc, je commence vraiment le jeu
# ici on gère les éléments de jeu
# (les grilles, les bateaux, les tirs, les tours et la victoire)

# pour les tours
joueur_actuel = 1  # 1 ou 2

#chage le tour du joueur
def changer_tour():
    global joueur_actuel
    joueur_actuel = 2 if joueur_actuel == 1 else 1


# gestion des bateaux
# tailles des bateaux (clé = nom, valeur = taille)
TAILLES_BATEAUX = {
    "bateaudetaille_5": 5,
    "bateaudetaille_4": 4,
    "bateaudetaille_3": 3,
    "deuxiemebateaudetaille_3": 3,
    "bateaudetaille_2": 2
}

# liste complète des bateaux 
LISTE_BATEAUX = list(TAILLES_BATEAUX.keys())

# listes des bateaux à placer pour chaque joueur
bateaux_restants_j1 = LISTE_BATEAUX.copy()
bateaux_restants_j2 = LISTE_BATEAUX.copy()


# constantes pour les états des cases de la grille
VIDE = 0
BATEAU = 1
TOUCHE = 2
RATE = 3
COULE = 4


# grilles vides pour les deux joueurs
grille_joueur1 = [[VIDE] * 10 for _ in range(10)]
grille_joueur2 = [[VIDE] * 10 for _ in range(10)]

#avoir la grille correspondant au joueur
def grille_joueur(joueur):
    return grille_joueur1 if joueur == 1 else grille_joueur2


#avoir la taille du bateau à partir de son nom
def taille_bateau(nom):
    return TAILLES_BATEAUX.get(nom)

# vérifier si un bateau peut être placé sans dépasser ou chevaucher un autre bateau
def peut_placer(grille, ligne, col, taille, horizontal=True):
    
    if horizontal:
        if col + taille > 10:
            return False
        for i in range(taille):
            if grille[ligne][col + i] == BATEAU:
                return False
    else:
        if ligne + taille > 10:
            return False
        for i in range(taille):
            if grille[ligne + i][col] == BATEAU:
                return False
    return True


# placement aléatoire des bateaux pour un joueur
def placement_aleatoire(joueur):

    # vider la grille
    grille = grille_joueur(joueur)
    for i in range(10):
        for j in range(10):
            grille[i][j] = VIDE

    # RESET des bateaux restants
    if joueur == 1:
        global bateaux_restants_j1
        bateaux_restants_j1 = LISTE_BATEAUX.copy()
    else:
        global bateaux_restants_j2
        bateaux_restants_j2 = LISTE_BATEAUX.copy()

    import random
    for bateau in LISTE_BATEAUX:
        taille = taille_bateau(bateau)
        place_ok = False
        while not place_ok: #eviter les chevauchements
            horizontal = random.choice([True, False])
            ligne = random.randint(0, 9)
            col = random.randint(0, 9)
            place_ok = peut_placer(grille, ligne, col, taille, horizontal)
            if place_ok:
                placer_bateau(joueur, bateau, ligne, col, horizontal)




# placer un bateau sur la grille du joueur si possible
def placer_bateau(joueur, nom_bateau, ligne, col, horizontal):

    if nom_bateau not in bateaux_restants_joueur(joueur):
             return False

    taille = taille_bateau(nom_bateau)
    if taille is None:
        return False

    grille = grille_joueur(joueur)

    if not peut_placer(grille, ligne, col, taille, horizontal):
        return False

    # placement réel
    if horizontal:
        for i in range(taille):
            grille[ligne][col + i] = BATEAU
    else:
        for i in range(taille):
            grille[ligne + i][col] = BATEAU

    # on enlève le bateau de la liste
    retirer_bateau(joueur, nom_bateau)
    return True


# obtenir la liste des bateaux restants pour un joueur 
def bateaux_restants_joueur(joueur):
    return bateaux_restants_j1 if joueur == 1 else bateaux_restants_j2

# retirer un bateau de la liste des bateaux restants
def retirer_bateau(joueur, nom_bateau):
    if joueur == 1:
        bateaux_restants_j1.remove(nom_bateau)
    else:
        bateaux_restants_j2.remove(nom_bateau)


#reinitialiser les grilles 
def reset_jeu():
    global bateaux_restants_j1, bateaux_restants_j2, joueur_actuel
    bateaux_restants_j1 = LISTE_BATEAUX.copy()
    bateaux_restants_j2 = LISTE_BATEAUX.copy()
    joueur_actuel = 1

    for i in range(10):
     for j in range(10):
        grille_joueur1[i][j] = VIDE
        grille_joueur2[i][j] = VIDE

# fonction pr un bateau coulé
def bateau_coule(joueur, ligne, colonne):
    bateau = trouver_bateau(joueur, ligne, colonne)  # retourne liste de coordonnées du bateau
    return all(grilles[joueur][l][c] == TOUCHE for l, c in bateau)


#pour les coordonnées d'un bateau
def coord_bateau(joueur, ligne, colonne):
    return trouver_bateau(joueur, ligne, colonne)

#donner la v ictoire si tous les bateaux sont coulés
def verifier_victoire(joueur):
    for ligne in grilles[joueur]:
        for case in ligne:
            if case == BATEAU:
                return False
    return True
