# =================== INTERFACE PRINCIPALE ===================
import tkinter as tk
from tkinter.messagebox import showinfo
import fonction as fn
import jeu
import apparence as app


# ========== FENÊTRE PRINCIPALE ==========
root = tk.Tk()
root.title('Bataille navale')
root.geometry('780x550')
root.configure(bg=app.theme_actuel["bg"]) 


# ========== FRAMES ==========
f1 = tk.Frame(root)  # Menu principal
f2 = tk.Frame(root)  # Mode PvP
f3 = tk.Frame(root)  # Paramètres
f4 = tk.Frame(root)  # Sélection du mode de jeu
f5 = tk.Frame(root)  # Mode contre IA

# Afficher le premier frame
f1.pack(fill='both', expand=True)

# Liste de tous les frames (important pour les thèmes)
frames = [f1, f2, f3, f4, f5]

# Menu
fn.create_menu(root)


# ========== FRAME 1 : MENU PRINCIPAL ==========
fn.bouton(
    f1, [" ", "Start game", " "],
    200, 50, 16, 2, "bold", 0.3,
    command=lambda: fn.swap_frames(f1, f4)
)

fn.bouton(
    f1, [" ", "Parametres", " "],
    200, 50, 16, 2, "bold", 0.5,
    command=lambda: fn.swap_frames(f1, f3)
)


# ========== FRAME 3 : PARAMÈTRES ==========
tk.Label(f3, text="Choisir un thème", font=('Arial', 14, 'bold')).pack(pady=10)

fn.bouton(
    f3, [" ", "Thème Bleu", " "],
    200, 50, 15, 2, "bold", 0.3,
    command=lambda: app.changer_theme(app.THEME_BLEU, root, frames, boutons_pvp, boutons_ia)
)

fn.bouton(
    f3, [" ", "Thème Sombre", " "],
    200, 50, 15, 2, "bold", 0.5,
    command=lambda: app.changer_theme(app.THEME_SOMBRE, root, frames, boutons_pvp, boutons_ia)
)

fn.bouton(
    f3, [" ", "Thème Classique", " "],
    200, 50, 15, 2, "bold", 0.7,
    command=lambda: app.changer_theme(app.THEME_CLASSIQUE, root, frames, boutons_pvp, boutons_ia)
)

fn.bouton(
    f3, [" ", "Thème Rose", " "],
    200, 50, 15, 2, "bold", 0.9,
    command=lambda: app.changer_theme(app.THEME_ROSE, root, frames, boutons_pvp, boutons_ia)
)

tk.Button(f3, text='Retour', command=lambda: fn.swap_frames(f3, f1)).pack(pady=5)


# ========== FRAME 4 : SÉLECTION DU MODE DE JEU ==========
tk.Label(f4, text="Choisir le mode de jeu", font=('Arial', 14, 'bold')).pack(pady=20)
fn.bouton(
    f4, [" ", "Contre l'IA", " "],
    200, 50, 16, 2, "bold", 0.3,
    command=lambda: fn.start_ia(root, f4, f5)
)
fn.bouton(
    f4, [" ", "Contre un autre joueur", " "],
    200, 50, 16, 2, "bold", 0.5,
    command=lambda: fn.start_pvp(root, f4, f2)
)

tk.Button(f4, text='Retour', command=lambda: fn.swap_frames(f4, f1)).pack(pady=5)


# ========== FRAME 2 : MODE JOUEUR CONTRE JOUEUR ==========
tk.Label(f2, text='Bienvenue dans ma Bataille Navale ;D', font=('Arial',14,'bold')).pack(pady=10)

# Panneaux
p = tk.PanedWindow(f2, orient=tk.HORIZONTAL, width=665, height=440)
p.pack_propagate(False)
p.pack(side=tk.TOP, pady=2, padx=2)

panel1 = fn.panel(p, 120, 250, app.theme_actuel, 'Boat Preset')
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
        b = tk.Button(
            panel2,
            width=2,
            height=2,
            bg=app.theme_actuel["grid"],
            command=lambda l=i, c=j: fn.clic_placement_bateau(l, c, boutons_pvp, app.theme_actuel)
        )
        b.grid(row=i, column=j, sticky="nsew")
        ligne.append(b)
    boutons_pvp.append(ligne)

# Boutons de contrôle
tk.Button(
    f2,
    text="Placement aléatoire",
    command=lambda: fn.placement_aleatoire_interface(boutons_pvp, app.theme_actuel)
).pack(pady=10)

tk.Button(f2, text='Retour', command=lambda: fn.swap_frames(f2, f4)).pack(pady=5)



# ========== FRAME 5 : MODE CONTRE IA ==========
tk.Label(f5, text='Bienvenue dans ma Bataille Navale ;D', font=('Arial', 14, 'bold')).pack(pady=10)

p = tk.PanedWindow(f5, orient=tk.HORIZONTAL, width=665, height=440)
p.pack_propagate(False)
p.pack(fill='both', expand=True, pady=2, padx=2)


panel1 = fn.panel(p, 120, 250, app.theme_actuel, 'Boat Preset')
panel2 = fn.panel(p, 250, 600, app.theme_actuel, 'Interface de Jeu')

# ===== Petite grille : bateaux du joueur sur le panel1 =====
mini_grille_joueur = []

for i in range(10):
    ligne = []
    for j in range(10):
        b = tk.Label(
            panel1,
            width=1,
            height=1,
            bg=app.theme_actuel["grid"],
            relief="solid",
            borderwidth=1
        )
        b.grid(row=i, column=j, padx=1, pady=1)
        ligne.append(b)
    mini_grille_joueur.append(ligne)

# On n'ajoute pas panel1 pour l'instant, uniquement panel2
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
        b = tk.Button(
            panel2,
            bg=app.theme_actuel["grid"],
            command=lambda l=i, c=j: fn.clic_placement_bateau_ia(l, c, boutons_ia, app.theme_actuel, p, panel1, mini_grille_joueur)
        )
        b.grid(row=i, column=j, sticky="nsew")
        ligne.append(b)
    boutons_ia.append(ligne)

# Boutons de contrôle
tk.Button(
    f5,
    text="Placement aléatoire",
    command=lambda: fn.placement_aleatoire_interface_ia(boutons_ia, app.theme_actuel, mini_grille_joueur)
    ).pack(pady=10)

tk.Button(f5, text='Retour', command=lambda: fn.swap_frames(f5, f4)).pack(pady=5)


# ========== LANCEMENT DE L'APPLICATION ==========
root.mainloop()

