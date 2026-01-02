"""
fonction.py réexporte toutes les fonctions depuis les nouveaux modules

Les fonctions sont maintenant organisées dans :
- interface.py : création d'interface (boutons, menus, panneaux)
- placement.py : placement des bateaux (manuel, aléatoire, drag & drop)
- phase_tir.py : gestion de la phase de tir
- navigation.py : navigation entre les frames et modes de jeu
"""

# Importer tout depuis les nouveaux modules
from interface import *
from placement import *
from phase_tir import *
from navigation import *

# Maintenir les variables globales pour compatibilité
import navigation as nav
import placement as plc

# Rediriger les variables vers les bons modules
def __getattr__(name):
    """Permet d'accéder aux variables des sous-modules de manière transparente."""
    if name in ['root', 'f_phase_tir', 'frame_placement_pvp', 'frame_placement_ia']:
        return getattr(nav, name)
    elif name in ['joueur_en_placement', 'bateau_en_cours', 'orientation_horizontale', 
                  'preview_cases', 'drag_widgets_pvp', 'drag_widgets_ia', 
                  'orientation_label_pvp', 'orientation_label_ia', 'mode_actuel']:
        return getattr(plc, name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
