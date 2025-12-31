def start_pvp():
    """Lance le mode joueur contre joueur."""
    fn.swap_frames(f4, f2)
    root.after(100, lambda: showinfo("Placement des bateaux", "Joueur 1 : place tes bateaux en cliquant sur les cases."))