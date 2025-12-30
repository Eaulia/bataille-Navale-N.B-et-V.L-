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
#juste pour tester
grille_joueur1 = [[0]*10 for _ in range(10)]
grille_joueur2 = [[0]*10 for _ in range(10)]

# 0 = vide, 1 = bateau
grille_joueur1[2][3] = 1
grille_joueur1[2][4] = 1
grille_joueur1[2][5] = 1



#déterminer qui a gagné
def a_perdu(grille):
    for ligne in grille:
        if BATEAU in ligne:
            return False
    return True