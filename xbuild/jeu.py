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