"""
sons.py - Gestionnaire de sons pour la Bataille Navale
Utilise pygame.mixer pour jouer les fichiers WAV
"""

import pygame
import os

# Initialiser pygame.mixer
pygame.mixer.init()

# Dictionnaire pour stocker les sons chargés
SONS = {}

def charger_sons():
    """
    Charge tous les fichiers WAV au démarrage du jeu.
    À appeler une seule fois au début du programme.
    """
    # Dossier contenant les sons
    dossier_sons = "sons"
    
    # Liste des sons à charger
    fichiers_sons = {
        "touche": "TOUCHE.wav",
        "coule": "COULE.wav",
        "rate": "RATE.wav",
        "victoire": "VICTOIRE.wav",
        "ambiance": "AMBIANCE.wav",  # Musique de fond 
    }
    
    for nom, fichier in fichiers_sons.items():
        chemin = os.path.join(dossier_sons, fichier)
        try:
            if os.path.exists(chemin):
                SONS[nom] = pygame.mixer.Sound(chemin)
                print(f"✅ Son chargé : {nom}")
            else:
                print(f"⚠️  Fichier manquant : {chemin}")
                SONS[nom] = None
        except Exception as e:
            print(f"Erreur chargement {nom}: {e}")
            SONS[nom] = None


def jouer_son(nom, volume=1.0):
    """
    Joue un son.
    
    Args:
        nom: Nom du son ("tir", "touche", "coule", etc.)
        volume: Volume entre 0.0 et 1.0
    """
    if nom in SONS and SONS[nom] is not None:
        try:
            SONS[nom].set_volume(volume)
            SONS[nom].play()
        except Exception as e:
            print(f"Erreur lecture son {nom}: {e}")
    else:
        print(f"⚠️  Son {nom} non disponible")


def jouer_musique(nom, loop=-1, volume=0.3):
    """
    Joue une musique de fond en boucle.
    
    Args:
        nom: Nom de la musique
        loop: -1 pour boucle infinie, 0 pour une seule fois
        volume: Volume entre 0.0 et 1.0
    """
    if nom in SONS and SONS[nom] is not None:
        try:
            SONS[nom].set_volume(volume)
            SONS[nom].play(loops=loop)
        except Exception as e:
            print(f"Erreur lecture musique {nom}: {e}")

# Charger les sons au démarrage du module
charger_sons()