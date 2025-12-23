import tkinter as tk
import fonction as fn


#différents thèmes de couleurs
THEME_BLEU = {
    "bg": "#006E6E",
    "frame": "#006E6E",
    "grid": "lightblue",
    "button": "#4FA3A3",
    "text": "white"
}

THEME_SOMBRE = {
    "bg": "#1E1E1E",
    "frame": "#1E1E1E",
    "grid": "#444444",
    "button": "#333333",
    "text": "white"
}

#choix du thème actuel
theme_actuel = THEME_BLEU

# FENETRE, création et affichage du titre et de la taille
# ";" sert à séparer les instructions sur une même ligne
root = tk.Tk(); root.title('Bataille navale'); root.geometry('650x400'); root.configure(bg=theme_actuel["bg"])

# FRAMES
f1 = tk.Frame(root); f1.pack(fill='both', expand=True)
f2 = tk.Frame(root)
f3 = tk.Frame(root)

def appliquer_theme(theme):
    global theme_actuel
    theme_actuel = theme

    # pour la fenêtre
    root.configure(bg=theme["bg"])

    # pour les frames
    f1.configure(bg=theme["frame"])
    f2.configure(bg=theme["frame"])
    f3.configure(bg=theme["frame"])

    # pour la grille boutons 
    for ligne in boutons:
        for b in ligne:
            b.config(bg=theme["grid"])

#pour tester le clic sur une case du grillage
def clic_case(ligne, colonne):
    print(ligne, colonne)

#MENU
fn.create_menu(root)


# BOUTONS
fn.bouton(f1, [" ", "Start game", " "], 200, 50, 16, 2, "bold", 0.3,
          command=lambda: fn.swap_frames(f1,f2))

fn.bouton(f1, [" ", "Parametres", " "], 200, 50, 16, 2, "bold", 0.5,
          command=lambda: fn.swap_frames(f1,f3))
          


# START FRAME 2
tk.Label(f2, text='Bienvenue dans ma Bataille Navale ;D', font=('Arial',14,'bold')).pack(pady=10)

# PANNEAUX
p = tk.PanedWindow(f2, orient=tk.HORIZONTAL, width=560, height=250)
p.pack_propagate(False)
p.pack(side=tk.TOP, pady=2, padx=2)

panel1 = fn.panel(p, 120, 250, '#7d9ab5', 'Boat Preset') ; p.add(panel1)
panel2 = fn.panel(p, 250, 600, '#97b3ce', 'Interface de Jeu') ; p.add(panel2)

# afficher une grille de boutons 10x10 dans panel2
boutons = []

for i in range(10):
    ligne = []
    for j in range(10):
        b = tk.Button(
            panel2,
            width=3,
            height=1,
            bg='lightblue',
            command=lambda l=i, c=j: clic_case(l, c)
        )
        b.grid(row=i, column=j)
        ligne.append(b)
    boutons.append(ligne)


tk.Button(f2, text='Retour', command=lambda: fn.swap_frames(f2,f1)).pack(pady=5)
tk.Button(f3, text='Retour', command=lambda: fn.swap_frames(f3,f1)).pack(pady=5)

#bouton pour changer le thème
tk.Label(f3, text="Choisir un thème", font=('Arial', 14, 'bold')).pack(pady=10)

tk.Button(f3, text="Thème Bleu", command=lambda: appliquer_theme(THEME_BLEU)).pack(pady=5)
tk.Button(f3, text="Thème Sombre", command=lambda: appliquer_theme(THEME_SOMBRE)).pack(pady=5)

root.mainloop()