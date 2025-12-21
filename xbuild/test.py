import tkinter as tk

def swap_frames(hide, show):
    """Echanger un frame en arrière-plan et un frame au premier plan.
    .pack_forget() sert à cacher un frame
    .pack(fill='both', expand=True) sert à afficher un frame
    """
    hide.pack_forget()
    show.pack(fill='both', expand=True)

# FENETRE, création et affichage du titre et de la taille
# ";" sert à séparer les instructions sur une même ligne
root = tk.Tk(); root.title('Bataille navale'); root.geometry('400x340')

# FRAMES
f1 = tk.Frame(root); f1.pack(fill='both', expand=True)
f2 = tk.Frame(root)
f3 = tk.Frame(root)

# BOUTON PERSONNALISÉ 
def bouton(parent, text_lines, wid, hei, size1, size2, boldd, relly, command=None):
    """
    parent: frame parent
    text_lines: text à afficher (liste de lignes)
    wid: longueur du bouton
    hei: hauteur du bouton
    size1: taille du texte principal
    size2: taille du texte secondaire
    command: lier la fonction et l'action 'le bouton est cliqué'

    .winfo_children() retourne la liste des widgets enfants d'un widget parent
    .bind() lie un événement (ici clic gauche) à une fonction
    """
    btn = tk.Frame(parent, width=wid, height=hei, bd=2, relief='raised')
    btn.place(relx=0.5, rely= relly, anchor='center'); btn.pack_propagate(False)
    for line in text_lines:
        if text_lines[1] == line:
            tk.Label(btn, text=line, font=('Helvetica',size1,boldd)).pack()
        else:
            tk.Label(btn, text=line, font=('Helvetica',size2)).pack()
    if command:
        def _on_click(event, cmd=command):
            """
            event: evenement (ex. clic gauche)
            cmd: fonction à appeler
            _on_click c'est si on clique sur le bouton 
            """
            cmd()
        for w in btn.winfo_children():
            w.bind('<Button-1>', _on_click)
        btn.bind('<Button-1>', _on_click)
    return btn

bouton(f1, [' ','Start game',' '], 150, 50, 16, 2, 'bold', 0.2, command=lambda: swap_frames(f1,f2))
bouton(f1, [' ','Parametres',' '], 150, 50, 16, 2, 'bold', 0.5, command=lambda: swap_frames(f1,f3))

tk.Label(f2, text='Bienvenue dans la Bataille Navale!', font=('Klee',14,'bold')).pack(pady=10)
tk.Button(f2, text='Retour', command=lambda: swap_frames(f2,f1)).pack(pady=5)
tk.Button(f3, text='Retour', command=lambda: swap_frames(f3,f1)).pack(pady=5)

root.mainloop()