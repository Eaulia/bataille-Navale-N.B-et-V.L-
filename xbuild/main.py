import tkinter as tk
import fonction as fn
from tkinter.messagebox import showinfo

def start_pvp():
    fn.swap_frames(f4, f2)
    # Affiche l’alerte pour demander aux joueurs de placer leurs bateaux
    showinfo("Placement des bateaux", "Joueur 1 : place tes bateaux en cliquant sur les cases.")



# différents thèmes de couleurs
THEME_BLEU = {"bg": "#006E6E","frame": "#006E6E","grid": "lightblue","button": "#4FA3A3","text": "white"}
THEME_SOMBRE = {"bg": "#1E1E1E","frame": "#1E1E1E","grid": "#444444","button": "#333333","text": "white"}
THEME_CLASSIQUE = {"bg": "#F0F0F0","frame": "#F0F0F0","grid": "white","button": "#E0E0E0","text": "black"}
THEME_ROSE = {"bg": "#FFB6C1","frame": "#FFB6C1","grid": "#FFDDEE","button": "#FF99AA","text": "black"}

# thème courant
theme_actuel = THEME_BLEU


# FENETRE, création et affichage du titre et de la taille 
# ";" sert à séparer les instructions sur une même ligne
root = tk.Tk()
root.title('Bataille navale')
root.geometry('780x550')
root.configure(bg=theme_actuel["bg"]) 


# FRAMES
f1 = tk.Frame(root)
f2 = tk.Frame(root)
f3 = tk.Frame(root)
f4 = tk.Frame(root)
f5 = tk.Frame(root)

# afficher le premier frame
f1.pack(fill='both', expand=True)

# liste de tous les frames (IMPORTANT pour les thèmes)
frames = [f1, f2, f3, f4, f5]

# MENU
fn.create_menu(root)

# BOUTONS FRAME 1
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


# fonction pour changer le thème
def changer_theme(theme):
    global theme_actuel
    theme_actuel = theme
    fn.appliquer_theme(theme_actuel, root, frames, boutons)


# PARAMETRES FRAME 3, les boutons pour changer le thème
tk.Label(f3, text="Choisir un thème", font=('Arial', 14, 'bold')).pack(pady=10)

fn.bouton(
    f3, [" ", "Thème Bleu", " "],
    200, 50, 15, 2, "bold", 0.3,
    command=lambda: changer_theme(THEME_BLEU)
)

fn.bouton(
    f3, [" ", "Thème Sombre", " "],
    200, 50, 15, 2, "bold", 0.5,
    command=lambda: changer_theme(THEME_SOMBRE)
)

fn.bouton(
    f3, [" ", "Thème Classique", " "],
    200, 50, 15, 2, "bold", 0.7,
    command=lambda: changer_theme(THEME_CLASSIQUE)
)

fn.bouton(
    f3, [" ", "Thème Rose", " "],
    200, 50, 15, 2, "bold", 0.9,
    command=lambda: changer_theme(THEME_ROSE)
)

tk.Button(f3, text='Retour', command=lambda: fn.swap_frames(f3, f1)).pack(pady=5)





# FRAME 4 (intermediaire pour choisir le mode de jeu)
tk.Label(f4, text="Choisir le mode de jeu", font=('Arial', 14, 'bold')).pack(pady=20)

# Boutons pour choisir entre IA ou joueur
fn.bouton(
    f4, [" ", "Contre l'IA", " "],
    200, 50, 16, 2, "bold", 0.3,
    command=lambda: fn.swap_frames(f4, f5)
)
fn.bouton(
    f4, [" ", "Contre un autre joueur", " "],
    200, 50, 16, 2, "bold", 0.5,
    command=lambda: start_pvp()

)
tk.Button(f4, text='Retour', command=lambda: fn.swap_frames(f4, f1)).pack(pady=5)





# FRAME 2, joueur contre joueur
tk.Label(f2, text='Bienvenue dans ma Bataille Navale ;D', font=('Arial',14,'bold')).pack(pady=10)

# PANNEAUX
p = tk.PanedWindow(f2, orient=tk.HORIZONTAL, width=665, height=440)
p.pack_propagate(False)
p.pack(side=tk.TOP, pady=2, padx=2)

panel1 = fn.panel(p, 120, 250, theme_actuel, 'Boat Preset')
panel2 = fn.panel(p, 250, 600, theme_actuel, 'Interface de Jeu')

p.add(panel1)
p.add(panel2)

# Configurer les lignes et colonnes de panel2 pour qu'elles prennent tout l'espace
for i in range(10):
    panel2.grid_columnconfigure(i, weight=1, uniform="equal")
    panel2.grid_rowconfigure(i, weight=1, uniform="equal")


# Afficher une grille de boutons 10x10 dans panel2
boutons = []

for i in range(10):
    ligne = []
    for j in range(10):
        b = tk.Button(
            panel2,
            width=2,
            height=2,
            bg=theme_actuel["grid"],
            command=lambda l=i, c=j: fn.clic_case(l, c)
        )
        b.grid(row=i, column=j, sticky="nsew")
        ligne.append(b)
    boutons.append(ligne)

# Essaie pour afficher un bateau horizontal de 3 cases
bateau = [(2, 3), (2, 4), (2, 5)]
for (l, c) in bateau:
    boutons[l][c].configure(bg="red")


tk.Button(f2, text='Retour', command=lambda: fn.swap_frames(f2, f4)).pack(pady=5)





# FRAME 5, joueur contre IA
tk.Label(f5, text='Bienvenue dans ma Bataille Navale ;D', font=('Arial',14,'bold')).pack(pady=10)

p = tk.PanedWindow(f5, orient=tk.HORIZONTAL, width=665, height=440)
p.pack_propagate(False)
p.pack(side=tk.TOP, pady=2, padx=2)

panel1 = fn.panel(p, 120, 250, theme_actuel, 'Boat Preset')
panel2 = fn.panel(p, 250, 600, theme_actuel, 'Interface de Jeu')

# Configurer les lignes et colonnes de panel2 pour qu'elles prennent tout l'espace
for i in range(10):
    panel2.grid_columnconfigure(i, weight=1, uniform="equal")
    panel2.grid_rowconfigure(i, weight=1, uniform="equal")

# Afficher une grille de boutons 10x10 dans panel2
boutons_ia = []

for i in range(10):
    ligne = []
    for j in range(10):
        b = tk.Button(
            panel2,
            width=2,
            height=2,
            bg=theme_actuel["grid"],
            command=lambda l=i, c=j: fn.clic_case(l, c)
        )
        b.grid(row=i, column=j, sticky="nsew")
        ligne.append(b)
    boutons_ia.append(ligne)

tk.Button(f5, text='Retour', command=lambda: fn.swap_frames(f5, f4)).pack(pady=5)

p.add(panel1)
p.add(panel2)

root.mainloop()
