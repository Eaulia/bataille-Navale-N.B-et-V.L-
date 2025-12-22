import tkinter as tk
import fonction as fn

# FENETRE, création et affichage du titre et de la taille
# ";" sert à séparer les instructions sur une même ligne
root = tk.Tk(); root.title('Bataille navale'); root.geometry('400x340')

#MENU
fn.create_menu(root)

# FRAMES
f1 = tk.Frame(root); f1.pack(fill='both', expand=True)
f2 = tk.Frame(root)
f3 = tk.Frame(root)


# BOUTONS
fn.bouton(f1, [' ','Start game',' '], 200, 50, 16, 2, 'bold', 0.3, command=lambda: fn.swap_frames(f1,f2))
fn.bouton(f1, [' ','Parametres',' '], 200, 50, 16, 2, 'bold', 0.5, command=lambda: fn.swap_frames(f1,f3))

# START FRAME 2
tk.Label(f2, text='Bienvenue dans MA Bataille Navale ;D', font=('Klee',14,'bold')).pack(pady=10)

# PANNEAUX
p = tk.PanedWindow(f2, orient=tk.HORIZONTAL, width=560, height=250)
p.pack_propagate(False)
p.pack(side=tk.TOP, pady=2, padx=2)

panel1 = fn.panel(p, 120, 250, '#7d9ab5', 'Boat Preset') ; p.add(panel1)
panel2 = fn.panel(p, 250, 600, '#97b3ce', 'Interface de Jeu') ; p.add(panel2)

tk.Button(f2, text='Retour', command=lambda: fn.swap_frames(f2,f1)).pack(pady=5)
tk.Button(f3, text='Retour', command=lambda: fn.swap_frames(f3,f1)).pack(pady=5)

root.mainloop()