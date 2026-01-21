"""
Module principal de l'application Bataille Navale.

Ce module gère :
- La création de la fenêtre principale
- La création et la gestion des différents frames (menus, modes de jeu, etc.)
- L'initialisation des grilles de jeu
- Le lancement de l'application
"""

import tkinter as tk
from tkinter.messagebox import showinfo
import fonction as fn
import apparence as app
import navigation as nav
import placement as plc
import sons

# ==================== FENÊTRE PRINCIPALE ====================

root = tk.Tk()
root.title('Bataille navale')
root.geometry('780x550')
root.configure(bg=app.theme_actuel["bg"]) 
sons.jouer_musique("ambiance", loop=-1, volume=0.1)


# ==================== CRÉATION DES FRAMES ====================

f1 = tk.Frame(root)  # Menu principal
f2 = tk.Frame(root)  # Mode PvP
f3 = tk.Frame(root)  # Paramètres
f4 = tk.Frame(root)  # Sélection du mode de jeu
f5 = tk.Frame(root)  # Mode contre IA
f6 = tk.Frame(root)  # Phase de tir

# Afficher le premier frame
f1.pack(fill='both', expand=True)

# Liste de tous les frames (important pour les thèmes)
frames = [f1, f2, f3, f4, f5]

# Initialiser les variables globales dans navigation.py
nav.root = root
nav.frame_placement_pvp = f2
nav.frame_placement_ia = f5

# Menu
fn.create_menu(root)


# ==================== FRAME 1 : MENU PRINCIPAL ====================

# Bouton "Start game"
fn.bouton(
    f1, [" ", "Start game", " "],
    200, 50, 16, 2, "bold", 0.3,
    commande=lambda: fn.swap_frames(f1, f4)
)

# Bouton "Paramètres"
fn.bouton(
    f1, [" ", "Parametres", " "],
    200, 50, 16, 2, "bold", 0.5,
    commande=lambda: fn.swap_frames(f1, f3)
)


# ==================== FRAME 3 : PARAMÈTRES ====================

tk.Label(f3, text="Choisir un thème", font=('Arial', 14, 'bold')).pack(pady=10)

fn.bouton(
    f3, [" ", "Thème Bleu", " "],
    200, 50, 15, 2, "bold", 0.3,
    commande=lambda: app.changer_theme(app.THEME_BLEU, root, frames, boutons_pvp, boutons_ia)
)

fn.bouton(
    f3, [" ", "Thème Sombre", " "],
    200, 50, 15, 2, "bold", 0.5,
    commande=lambda: app.changer_theme(app.THEME_SOMBRE, root, frames, boutons_pvp, boutons_ia)
)

fn.bouton(
    f3, [" ", "Thème Classique", " "],
    200, 50, 15, 2, "bold", 0.7,
    commande=lambda: app.changer_theme(app.THEME_CLASSIQUE, root, frames, boutons_pvp, boutons_ia)
)

fn.bouton(
    f3, [" ", "Thème Rose", " "],
    200, 50, 15, 2, "bold", 0.9,
    commande=lambda: app.changer_theme(app.THEME_ROSE, root, frames, boutons_pvp, boutons_ia)
)

# Bouton "Retour"
tk.Button(f3, text='Retour', command=lambda: fn.swap_frames(f3, f1)).pack(pady=5)


# ==================== FRAME 4 : SÉLECTION DU MODE DE JEU ====================

tk.Label(f4, text="Choisir le mode de jeu", font=('Arial', 14, 'bold')).pack(pady=20)

# Bouton "Contre l'IA"
fn.bouton(
    f4, [" ", "Contre l'IA", " "],
    200, 50, 16, 2, "bold", 0.3,
    commande=lambda: fn.start_ia(root, f4, f5)
)

# Bouton "Contre un autre joueur"
fn.bouton(
    f4, [" ", "Contre un autre joueur", " "],
    200, 50, 16, 2, "bold", 0.5,
    commande=lambda: fn.start_pvp(root, f4, f2)
)

# Bouton "Retour"
tk.Button(f4, text='Retour', command=lambda: fn.swap_frames(f4, f1)).pack(pady=5)


# ==================== FRAME 2 : MODE JOUEUR CONTRE JOUEUR (pas finit) ====================

tk.Label(f2, text='Bienvenue dans ma Bataille Navale ;D', font=('Arial',14,'bold')).pack(pady=10)

# Panneaux
p = tk.PanedWindow(f2, orient=tk.HORIZONTAL, width=665, height=440)
p.pack_propagate(False)
p.pack(side=tk.TOP, pady=2, padx=2)

panel1 = fn.panel(p, 200, 250, app.theme_actuel, 'Bateaux Disponibles')
panel2 = fn.panel(p, 250, 600, app.theme_actuel, 'Interface de Jeu')

p.add(panel1)
p.add(panel2)

# Configurer les lignes et colonnes de panel2 pour qu'elles prennent tout l'espace
for i in range(10):
    panel2.grid_columnconfigure(i, weight=1, uniform="equal")
    panel2.grid_rowconfigure(i, weight=1, uniform="equal")


# Grille de boutons 10x10 pour le placement des bateaux
boutons_pvp = []

for i in range(10):
    ligne = []
    for j in range(10):
        b = tk.Label(
            panel2,
            width=4,
            height=2,
            bg=app.theme_actuel["grid"],
            relief="raised",
            borderwidth=2
        )
        b.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
        b.bind("<Button-1>", lambda e, l=i, c=j: fn.clic_placement_bateau(l, c, boutons_pvp, app.theme_actuel))
        b.bind("<Motion>", lambda e, l=i, c=j: fn.previsualiser_placement(l, c, boutons_pvp, app.theme_actuel))
        ligne.append(b)
    boutons_pvp.append(ligne)

#rendre grille pvp accessible globalement
root.boutons_pvp = boutons_pvp

# Créer le panneau de bateaux disponibles
plc.drag_widgets_pvp, plc.orientation_label_pvp = fn.creer_panneau_bateaux(panel1, 1, app.theme_actuel)

# Fonction pour gérer la rotation 
def rotation_pvp(event):
    fn.rotation_touche_r()
    return "break"  # Empêche la propagation de l'événement

# Lier la touche R pour changer l'orientation - bind global sur root
root.bind("<KeyPress-r>", rotation_pvp)
root.bind("<KeyPress-R>", rotation_pvp)

# Boutons de contrôle
tk.Button(
    f2,
    text="Placement aléatoire",
    command=lambda: fn.placement_aleatoire_interface(boutons_pvp, app.theme_actuel)
).pack(pady=10)

# Bouton retour
tk.Button(f2, text='Retour', command=lambda: fn.swap_frames(f2, f4)).pack(pady=5)


# ====================== FRAME 5 : MODE CONTRE IA =======================

tk.Label(f5, text='Bienvenue dans ma Bataille Navale ;D', font=('Arial', 14, 'bold')).pack(pady=10)

# Créer les panneaux
p = tk.PanedWindow(f5, orient=tk.HORIZONTAL, width=665, height=440)
p.pack_propagate(False)
p.pack(fill='both', expand=True, pady=2, padx=2)

panel1 = fn.panel(p, 200, 250, app.theme_actuel, 'Bateaux Disponibles')
panel2 = fn.panel(p, 250, 600, app.theme_actuel, 'Interface de Jeu')

# Créer le panneau de bateaux disponibles dans panel1 (on l'ajoutera au paned window)
plc.drag_widgets_ia, plc.orientation_label_ia = fn.creer_panneau_bateaux(panel1, 1, app.theme_actuel)

# Ajouter panel1 avec les bateaux
p.add(panel1)
p.add(panel2)


# Configurer les lignes et colonnes de panel2 pour qu'elles prennent tout l'espace
for i in range(10):
    panel2.grid_columnconfigure(i, weight=1, uniform="equal")
    panel2.grid_rowconfigure(i, weight=1, uniform="equal")

# Grille de boutons 10x10 pour le placement des bateaux
boutons_ia = []

for i in range(10):
    ligne = []
    for j in range(10):
        b = tk.Label(
            panel2,
            width=4,
            height=2,
            bg=app.theme_actuel["grid"],
            relief="raised",
            borderwidth=2
        )
        b.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
        b.bind("<Button-1>", lambda e, l=i, c=j: fn.clic_placement_bateau_ia(l, c, boutons_ia, app.theme_actuel))
        b.bind("<Motion>", lambda e, l=i, c=j: fn.previsualiser_placement(l, c, boutons_ia, app.theme_actuel))
        ligne.append(b)
    boutons_ia.append(ligne)

#rendre grille ia accessible globalement
root.boutons_ia = boutons_ia

# Boutons de contrôle
tk.Button(
    f5,
    text="Placement aléatoire",
    command=lambda: fn.placement_aleatoire_interface_ia(boutons_ia, app.theme_actuel)
    ).pack(pady=10)

# Bouton retour
tk.Button(f5, text='Retour', command=lambda: fn.swap_frames(f5, f4)).pack(pady=5)


# ==================== FRAME 6 : PHASE DE TIR ====================

# Frame de la phase de tir
f_phase_tir = tk.Frame(root, bg="white")
nav.f_phase_tir = f_phase_tir

# Initialiser l'interface de tir (sera appelé plus tard)
# fn.initialiser_phase_tir(f_phase_tir, app.theme_actuel)


# ==================== LANCEMENT DE L'APPLICATION ====================

root.mainloop()
