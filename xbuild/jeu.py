#nouveau dossier après avoir fini l'interface etc, je commence vraiment le jeu
#ici on gère les éléments de jeu (les grilles, les bateaux, les tirs, les tours et la victoire)

#les tours 
joueur_actuel = 1

def changer_tour():
    global joueur_actuel
    joueur_actuel = 2 if joueur_actuel == 1 else 1


# les bateaux 
BATEAUX_PRESET = {
    "porte_avions": 5,
    "croiseur": 4,
    "sous_marin": 3,
    "sous_marin_2": 3,
    "torpilleur": 2
}


grille_joueur1 = [[0]*10 for _ in range(10)]  # grille vide pour le joueur 1
grille_joueur2 = [[0]*10 for _ in range(10)] # grille vide pour le joueur 2

#là les fonctions sont chiantes mais c'est juste pour pas qu'on puisse placer plus de bateaux que prévu

# pour placement selon le preset
placement_en_cours = True
liste_bateaux = list(BATEAUX_PRESET.values())  # valeurs des bateaux à placer
indice_bateau = 0  # quel bateau on place maintenant

# renvoie taille du bateau qu'on place actuellement
def bateau_en_cours_taille():
    if indice_bateau < len(liste_bateaux):
        return liste_bateaux[indice_bateau]
    return None

#true si le bateau peut être placé partir de (ligne, col) dans la grille sans dépasser
def peut_placer(grille, ligne, col, taille, horizontal=True):
    if horizontal:
        if col + taille > 10:
            return False
        for i in range(taille):
            if grille[ligne][col+i] == 1:
                return False
    else:
        if ligne + taille > 10:
            return False
        for i in range(taille):
            if grille[ligne+i][col] == 1:
                return False
    return True

#place ENFFIN un bateau dans la grille, si possible
def placer_bateau(grille, ligne, col, taille, horizontal):
    if not peut_placer(grille, ligne, col, taille, horizontal): #on verifie
        return False

    if horizontal:
        for i in range(taille):
            grille[ligne][col+i] = 1
    else:
        for i in range(taille):
            grille[ligne+i][col] = 1
    return True



# pour placer bateau dans la grille
def placer_bateau_j1(ligne, colonne) :
    if grille_joueur1[ligne][colonne] == 0:
        grille_joueur1[ligne][colonne] = 1
        return True #case vide donc on peut placer le bateau
    return False #case déjà occupée


#déterminer qui a gagné
def a_perdu(grille):
    for ligne in grille:
        if BATEAU in ligne:
            return False
    return True