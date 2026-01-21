"""
Module de gestion CSV.

Ce module contient :
- La fonction pour enregistrer les statistiques des parties dans un fichier CSV

"""

import csv
from datetime import datetime

FICHIER_CSV = "stats_parties.csv"

def enregistrer_partie(mode, vainqueur, coups_joueur, coups_ia):
    """
    Enregistre les infos d'une partie dans un fichier CSV.
    """
    with open(FICHIER_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # écrire l'en-tête si le fichier est vide
        if f.tell() == 0:
            writer.writerow([
                "date",
                "mode",
                "vainqueur",
                "coups_joueur",
                "coups_ia"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            mode,
            vainqueur,
            coups_joueur,
            coups_ia
        ])
