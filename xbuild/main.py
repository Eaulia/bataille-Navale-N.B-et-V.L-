import tkinter as tk
import fonction as fn


#différents thèmes de couleurs
THEME_BLEU = {"bg": "#006E6E","frame": "#006E6E","grid": "lightblue","button": "#4FA3A3","text": "white"}
THEME_SOMBRE = {"bg": "#1E1E1E","frame": "#1E1E1E","grid": "#444444","button": "#333333","text": "white"}
THEME_CLASSIQUE = {"bg": "#F0F0F0","frame": "#F0F0F0","grid": "white","button": "#E0E0E0","text": "black"}

theme_actuel = THEME_BLEU


# FENETRE, création et affichage du titre et de la taille 
# ";" sert à séparer les instructions sur une même ligne
root = tk.Tk(); root.title('Bataille navale'); root.geometry('780x550'); root.configure(bg=theme_actuel["bg"]) 


# FRAMES
f1 = tk.Frame(root); f1.pack(fill='both', expand=True)
f2 = tk.Frame(root)
f3 = tk.Frame(root)
f4 = tk.Frame(root)

#MENU
fn.create_menu(root)

# BOUTONS FRAME 1
fn.bouton(f1, [" ", "Start game", " "], 200, 50, 16, 2, "bold", 0.3,command=lambda: fn.swap_frames(f1,f4))
fn.bouton(f1, [" ", "Parametres", " "], 200, 50, 16, 2, "bold", 0.5, command=lambda: fn.swap_frames(f1,f3))


# PARAMETRES FRAME 3 : boutons pour changer le thème
tk.Label(f3, text="Choisir un thème", font=('Arial', 14, 'bold')).pack(pady=10)

fn.bouton(f3, [" ", "Thème Bleu", " "], 200, 50, 15, 2, "bold", 0.3, command=lambda: fn.appliquer_theme(THEME_BLEU, root, f1, f2, f3, boutons))
fn.bouton(f3, [" ", "Thème Sombre", " "], 200, 50, 15, 2, "bold", 0.5, command=lambda: fn.appliquer_theme(THEME_SOMBRE, root, f1, f2, f3, boutons))
fn.bouton(f3, [" ", "Thème Classique", " "], 200, 50, 15, 2, "bold", 0.7, command=lambda: fn.appliquer_theme(THEME_CLASSIQUE, root, f1, f2, f3, boutons))

tk.Button(f3, text='Retour', command=lambda: fn.swap_frames(f3,f1)).pack(pady=5)


# FRAME 4 (intermediaire pour choisir le mode de jeu)
tk.Label(f4, text="Choisir le mode de jeu", font=('Arial', 14, 'bold')).pack(pady=20)

# Boutons pour choisir entre IA ou joueur
fn.bouton(f4, [" ", "Contre l'IA", " "], 200, 50, 16, 2, "bold", 0.3, command=lambda: fn.swap_frames(f4, f2))  # Aller à la page de jeu
fn.bouton(f4, [" ", "Contre un autre joueur", " "], 200, 50, 16, 2, "bold", 0.5, command=lambda: fn.swap_frames(f4, f2))  # Aller à la page de jeu
# Appliquer le thème à f4
f4.configure(bg=theme_actuel["frame"])



# START FRAME 2
tk.Label(f2, text='Bienvenue dans ma Bataille Navale ;D', font=('Arial',14,'bold')).pack(pady=10)

# PANNEAUX
p = tk.PanedWindow(f2, orient=tk.HORIZONTAL, width=665, height=440)
p.pack_propagate(False)
p.pack(side=tk.TOP, pady=2, padx=2)

panel1 = fn.panel(p, 120, 250, '#7d9ab5', 'Boat Preset') ; p.add(panel1)
panel2 = fn.panel(p, 250, 600, '#97b3ce', 'Interface de Jeu') ; p.add(panel2)

# Configurer les lignes et colonnes de panel2 pour qu'elles prennent tout l'espace
for i in range(10):
    panel2.grid_columnconfigure(i, weight=1, uniform="equal")  # Uniforme et redimensionnable
    panel2.grid_rowconfigure(i, weight=1, uniform="equal")  # Uniforme et redimensionnable

# Afficher une grille de boutons 10x10 dans panel2
boutons = []

for i in range(10):
    ligne = []
    for j in range(10):
        b = tk.Button(panel2, width=2, height=2, bg='lightblue', command=lambda l=i, c=j: fn.clic_case(l, c))
        b.grid(row=i, column=j, sticky="nsew")  # Le bouton occupe toute la cellule de la grille
        ligne.append(b)
    boutons.append(ligne)

tk.Button(f2, text='Retour', command=lambda: fn.swap_frames(f2,f1)).pack(pady=5)

root.mainloop()