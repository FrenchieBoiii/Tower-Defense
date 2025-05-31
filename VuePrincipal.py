import tkinter as tk 
from PIL import Image, ImageTk
from tkinter import scrolledtext

from Controleur import Controleur


class VuePresentation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Royal Defense")
        self.geometry("780x440")
        self.resizable(False, False)
       
        self.creer_widgets()

    def creer_widgets(self):
        """
        Crée et positionne tous les widgets de l'écran d'accueil, y compris le fond d'écran,
        le titre du jeu et les boutons d'action.
        """
        self.canvas_presentation = tk.Canvas(self, width=780, height=440, highlightthickness=0)
        self.canvas_presentation.pack(fill="both", expand=True)
        
        self.bg_image = ImageTk.PhotoImage(file="images/fond_ecran.png")
        self.canvas_presentation.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        self.canvas_presentation.create_text(390, 100,text="⚔ Royal Defense ⚔",font=("Algerian", 48, "bold"),fill="#6A0D0D",anchor="center")
        
        self.bouton_lancer_jeu = tk.Button(self,text="Entrer dans la bataille",font=("Georgia", 16, "bold"),bg="#6A0D0D",fg="white",
                                           activebackground="#8B1A1A",activeforeground="white",relief="raised",bd=4,command=self.ouvrir_fenetre_jeu)

        self.bouton_quitter = tk.Button(self,text="Abandonner le royaume",font=("Georgia", 14),bg="#5A0B0B",fg="white",activebackground="#7A1313",
                                        activeforeground="white",relief="ridge",bd=3,command=self.quitter)

        self.canvas_presentation.create_window(390, 200, window=self.bouton_lancer_jeu, width=300, height=40)
        self.canvas_presentation.create_window(390, 280, window=self.bouton_quitter, width=220, height=35)

    def quitter(self):
        """
        Ferme la fenêtre de présentation.
        """
        self.destroy()

    def ouvrir_fenetre_jeu(self):
        """
        Ouvre la fenêtre principale du jeu (VuePrincipale) et bloque l'interaction avec la
        fenêtre actuelle tant qu'elle est ouverte.
        """
        fenetre_jeu = VuePrincipale(self, 1000, 700)
        fenetre_jeu.grab_set()


class VuePrincipale(tk.Toplevel):
    def __init__(self, parent, l_canvas=900, h_canvas=700,):        
        super().__init__(parent)
        self.title("Fenêtre de jeu")
        self.geometry(f"{l_canvas}x{h_canvas}")
        self.resizable(False, False)
        
        self.controleur = Controleur()
        self.grille = self.controleur.grille

        self.taille_case = 20
        self.largeur = len(self.grille[0]) * self.taille_case
        self.hauteur = len(self.grille) * self.taille_case
        self.sprites = {}
        self.tiles_occupees = []
        
        self.load_all_sprites("images/pont.png", 1, 1, tile_size=20, prefix="wood_")
        self.load_all_sprites("images/sang.png", 1, 1, tile_size=16, prefix="sang_")
        self.load_all_sprites("images/tileset3.png", 4, 4, tile_size=20, prefix="tile3_")
        self.load_all_sprites("images/tileset.png", 7, 52, tile_size=16, prefix="ennemi_")
        
        self.creer_widgets()
        
        self.mode_placement = False
        self.wave_en_cours = self.controleur.wave_en_cours

    def creer_widgets(self):
        """
        Crée tous les éléments graphiques de l'interface de jeu : canvas, boutique,
        barre de vie, zones d'information et boutons.
        """
        frame_global = tk.Frame(self)
        frame_global.pack(fill="both", expand=True)

        frame_haut = tk.Frame(frame_global, bg="#2e1a12")
        frame_haut.pack(side="top", fill="x", pady=5)
        self.label_defenses = tk.Label(frame_haut, text="⚔ Royal Defense ⚔", font=("Algerian", 20, "bold"), fg="#8b0000", bg="#2e1a12")
        self.label_defenses.pack(pady=5)
    
        hp_frame = tk.Frame(frame_haut, bg="#2e1a12")
        hp_frame.pack(side="left", padx=10)
        tk.Label(hp_frame, text="HP :", font=("Arial", 12), bg="#2e1a12", fg="white").pack(side="left", padx=5)
        self.barre_vie = tk.Canvas(hp_frame, width=200, height=20, bg="gray")
        self.barre_vie.pack(side="left")
        self.maj_barre_vie()
    
        frame_centre = tk.Frame(frame_global)
        frame_centre.pack(fill="both", expand=True, padx=10, pady=10)
    
        canvas_container = tk.Frame(frame_centre)
        canvas_container.pack(side="left", expand=True, padx=20)
    
        self.canvas = tk.Canvas(canvas_container,width=self.largeur,height=self.hauteur,highlightthickness=0,bg="white")
        self.canvas.pack()
        self.remplir_grille()
        self.canvas.bind("<Button-1>", self.placer_defense)
    
        boutique = tk.Frame(frame_centre, width=250, bg="#e0c097")
        boutique.pack(side="right", fill="y", padx=10)
    
        frame_argent = tk.LabelFrame(boutique, text="Or :", font=("Arial", 12, "bold"), fg="gold", bg="#e0c097")
        frame_argent.pack(pady=5, padx=10, fill="x")
        self.label_argent = tk.Label(frame_argent, text=str(self.controleur.argent), font=("Arial", 16, "bold"), fg="gold", bg="#e0c097")
        self.label_argent.pack(padx=10, pady=2)
    
        label_boutique = tk.Label(boutique, text="Boutique", font=("Georgia", 14, "bold"), bg="#e0c097", fg="#4b2e2e")
        label_boutique.pack(pady=5)
    
        self.choix = tk.StringVar(value="archer")
        
        tk.Radiobutton(boutique, text="Tour d'archer : 25 or", variable=self.choix, value="archer",bg="#e0c097", anchor="w").pack(fill="x", padx=10)
        tk.Radiobutton(boutique, text="Tour de mage : 50 or", variable=self.choix, value="mage",bg="#e0c097", anchor="w").pack(fill="x", padx=10)
        tk.Radiobutton(boutique, text="Tour de baliste : 80 or", variable=self.choix, value="baliste",bg="#e0c097", anchor="w").pack(fill="x", padx=10)
        tk.Radiobutton(boutique, text="Tour de feu : 60 or", variable=self.choix, value="feu",bg="#e0c097", anchor="w").pack(fill="x", padx=10)
        tk.Radiobutton(boutique, text="Muraille : 10 or", variable=self.choix, value="muraille",bg="#e0c097", anchor="w").pack(fill="x", padx=10)
    
        bouton_style = {
            "font": ("Georgia", 12, "bold"),
            "bg": "#6A0D0D",
            "fg": "white",
            "activebackground": "#8B1A1A",
            "activeforeground": "white",
            "relief": "raised",
            "bd": 3
        }
    
        bouton_accepter = tk.Button(boutique, text="Accepter", command=self.accepter_defense, **bouton_style)
        bouton_accepter.pack(pady=10)
    
        self.aide = scrolledtext.ScrolledText(boutique, wrap=tk.WORD, width=30, height=8,font=("Times New Roman", 11), bg="#fdf6e3", fg="#3b1f1f")
        self.aide.insert(tk.INSERT, "Bienvenue dans Royal Defense !\n\nChoisissez une défense à poser.")
        self.aide.pack(padx=10, pady=10)

        frame_bas = tk.Frame(frame_global, bg="#2e1a12")
        frame_bas.pack(side="bottom", fill="x", pady=5)
    
        self.bouton_wave = tk.Button(frame_bas, text="☠ Lancer la vague", command=self.lancer_wave, **bouton_style)
        self.bouton_wave.pack(pady=5)
    
        self.label_wave = tk.Label(frame_bas, text="Wave 1", font=("Arial", 12, "bold"), bg="#2e1a12", fg="white")
        self.label_wave.pack(side="left", padx=10)
    
        bouton_fermer = tk.Button(frame_bas, text="Fermer", command=self.destroy, **bouton_style)
        bouton_fermer.pack(side="right", padx=10)
    
    def load_all_sprites(self, tileset_path, cols, rows, tile_size, prefix=""):
        """
        Charge un tileset découpé en sprites individuels stockés dans un dictionnaire.

        Entrées :
            tileset_path: string du chemin vers l'image du tileset
            cols: entier, nombre de colonnes dans le tileset
            rows: entier, nombre de lignes dans le tileset
            tile_size: entier, taille d’un sprite en pixels (carré)
            prefix: string décrivant le préfixe à ajouter aux clés du dictionnaire de sprites
        """
        tileset = Image.open(tileset_path)
        for y in range(rows):
            for x in range(cols):
                box = (x * tile_size, y * tile_size, (x + 1) * tile_size, (y + 1) * tile_size)
                sprite_img = tileset.crop(box)
                sprite_img = sprite_img.resize((self.taille_case, self.taille_case), Image.Resampling.LANCZOS)
                key = f"{prefix}{x}_{y}"
                self.sprites[key] = ImageTk.PhotoImage(sprite_img)

    def accepter_defense(self):
        """
        Active le mode de placement d'une défense sélectionnée par l'utilisateur
        et affiche un message dans le champ d'aide.
        """
        self.mode_placement = True
        self.aide.insert(tk.END, f"\n\nVous avez choisi : {self.choix.get()}\nCliquez sur le canvas pour placer.")
        self.aide.see(tk.END)
        
    def placer_defense(self, event):
        """
        Place une défense sur la grille si le mode de placement est actif et que
        l'utilisateur clique sur une case. Met à jour le canvas et l'état du jeu.

        Entrée :
            event: événement de clic souris contenant la position de la souris
        """
        if self.mode_placement:
            col = event.x // self.taille_case
            row = event.y // self.taille_case
            type_def = self.choix.get()
            
            reussi, message = self.controleur.placer_defense(row, col, type_def)
            self.aide.insert(tk.END, f"\n{message}")
            self.aide.see(tk.END)
            
            if reussi:
                self.dessiner_defense(row, col, type_def)
                self.label_argent.config(text=str(self.controleur.argent))
                self.mode_placement = False
        
    def dessiner_defense(self, row, col, type_def):
        """
        Affiche le sprite correspondant à la défense choisie à la position spécifiée.

        Entrées :
            row: entier indiquant la ligne de la grille
            col: entier indiquant la colonne de la grille
            type_def: string indiquant le type de défense à dessiner (archer, mage, etc.)
        """
        if type_def == "archer":
            archer = self.sprites["tile3_1_3"]
            self.canvas.create_image(col*self.taille_case, row*self.taille_case, image=archer, anchor='nw')
            self.canvas.archer = archer
        elif type_def == "mage":
            mage = self.sprites["tile3_1_2"]
            self.canvas.create_image(col*self.taille_case, row*self.taille_case, image=mage, anchor='nw')
            self.canvas.mage = mage
        elif type_def == "baliste":
            baliste = self.sprites["tile3_2_2"]
            self.canvas.create_image(col*self.taille_case, row*self.taille_case, image=baliste, anchor='nw')
            self.canvas.baliste = baliste
        elif type_def == "feu":
            feu = self.sprites["tile3_0_3"]
            self.canvas.create_image(col*self.taille_case, row*self.taille_case, image=feu, anchor='nw')
            self.canvas.feu = feu
        elif type_def == "muraille":
            muraille = self.sprites["tile3_2_3"]
            self.canvas.create_image(col*self.taille_case, row*self.taille_case, image=muraille, anchor='nw')
            self.canvas.muraille = muraille

    def dessiner_ennemis(self):
        """
        Affiche tous les ennemis actifs sur le canvas en fonction de leur position
        et de leur type.
        """
        self.canvas.delete("ennemi")
        self.tiles_occupees = []
        for ennemi in self.controleur.ennemis:
            row, col = ennemi.coord
            self.tiles_occupees.append((row, col))
            x1 = col * self.taille_case
            y1 = row * self.taille_case
            if ennemi.type_ennemi == "archer":
                archer = self.sprites["ennemi_0_16"]
                self.canvas.create_image(x1, y1, image=archer, anchor='nw', tags="ennemi")
            elif ennemi.type_ennemi == "paysan":
                paysan = self.sprites["ennemi_1_16"]
                self.canvas.create_image(x1, y1, image=paysan, anchor='nw', tags="ennemi")
            elif ennemi.type_ennemi == "chevalier":
                chevalier = self.sprites["ennemi_3_16"]
                self.canvas.create_image(x1, y1, image=chevalier, anchor='nw', tags="ennemi")
            elif ennemi.type_ennemi == "catapulte":
                catapulte = self.sprites["ennemi_4_16"]
                self.canvas.create_image(x1, y1, image=catapulte, anchor='nw', tags="ennemi")
            elif ennemi.type_ennemi == "bandit":
                bandit = self.sprites["ennemi_5_16"]
                self.canvas.create_image(x1, y1, image=bandit, anchor='nw', tags="ennemi")
            elif ennemi.type_ennemi == "seigneur":
                seigneur = self.sprites["ennemi_2_16"]
                self.canvas.create_image(x1, y1, image=seigneur, anchor='nw', tags="ennemi")
    
    def dessiner_sang(self):
        """
        Dessine des taches de sang sur le canvas aux emplacements où des ennemis
        ont été éliminés, sauf si une autre entité y est présente.
        """
        for coord in self.controleur.sang:
            if coord not in self.tiles_occupees:
                x1 = coord[1] * self.taille_case
                y1 = coord[0] * self.taille_case
                sang = self.sprites["sang_0_0"]
                self.canvas.create_image(x1, y1, image=sang, anchor='nw',tags="sang")
                        
    def lancer_tic(self):
        """
        Gère le déroulement d’un "tic" de jeu : met à jour les ennemis, le sang,
        la vie et l’argent. Planifie le prochain tic si nécessaire.
        """
        encore = self.controleur.prochain_tic()
        self.dessiner_ennemis()
        self.dessiner_sang()
        self.maj_barre_vie()
        self.label_argent.config(text=str(self.controleur.argent))
        if encore:
            self.after(500, self.lancer_tic)
        else:
            self.canvas.delete("sang")
            self.controleur.wave_terminee()
            self.aide.see(tk.END)
            if self.controleur.est_game_over():
                self.aide.insert(tk.END,"\n\n\nVous avez perdu ! Fermez la fenêtre pour relancer une partie.")
            elif self.controleur.a_gagne():
                self.aide.insert(tk.END,"\n\n\nBravo, vous avez survécu à toutes les vagues ! Fermez la fenêtre pour relancer une partie.")
            else:
                self.aide.insert(tk.END,"\n\n\nC'est la fin de la wave. Bravo vous avez survécu ! \nVous pouvez replacer des défenses.")     

                
    def lancer_wave(self):
        """
        Démarre une nouvelle vague d'ennemis et met à jour l'affichage du numéro
        de vague. Lance les tics de jeu.
        """
        self.controleur.demarrer_wave()
        self.label_wave.config(text=f"Wave {self.controleur.numero_wave}")
        self.lancer_tic()

    def maj_barre_vie(self):
        """
        Met à jour graphiquement la barre de vie du joueur en fonction de la
        vie actuelle, avec une couleur variant selon le pourcentage.
        """
        self.barre_vie.delete("all")
        vie = self.controleur.vie
        largeur = int((vie / 100) * 200)
        couleur = "green" if vie > 50 else "orange" if vie > 20 else "red"
        self.barre_vie.create_rectangle(0, 0, largeur, 20, fill=couleur)

    def remplir_grille(self):
        """
        Dessine la carte du jeu en parcourant la grille et en plaçant les éléments
        graphiques correspondant au type de terrain (herbe, forêt, rivière, etc.).
        """
        self.herbe_images = []
        self.montagnes_images = []
        self.riviere_images = []
        self.foret_images = []
        self.pont_images = []
        for row in range(len(self.grille)):
            for col in range(len(self.grille[row])):
                x1 = col * self.taille_case
                y1 = row * self.taille_case
                herbe = self.sprites["tile3_3_0"]
                self.canvas.create_image(x1, y1, image=herbe, anchor='nw')
                self.herbe_images.append(herbe)
                if self.grille[row][col] == 'Montagne':
                    montagne = self.sprites["tile3_2_0"]
                    self.canvas.create_image(x1, y1, image=montagne, anchor='nw')
                    self.montagnes_images.append(montagne)
                elif self.grille[row][col] == 'Riviere':
                    riviere = self.sprites["tile3_3_3"]
                    self.canvas.create_image(x1, y1, image=riviere, anchor='nw')
                    self.riviere_images.append(riviere)
                elif self.grille[row][col] == 'Foret':
                    foret = self.sprites["tile3_0_0"]
                    self.canvas.create_image(x1, y1, image=foret, anchor='nw')
                    self.foret_images.append(foret)
                elif self.grille[row][col] == 'Pont':
                    pont = self.sprites["wood_0_0"]
                    self.canvas.create_image(x1, y1, image=pont, anchor='nw')
                    self.pont_images.append(pont)
                elif self.grille[row][col] == 'Depart':
                    depart = self.sprites["ennemi_6_4"]
                    self.canvas.create_image(x1, y1, image=depart, anchor='nw')
                elif self.grille[row][col] == 'Arrivee':
                    arrivee = self.sprites["ennemi_6_4"]
                    self.canvas.create_image(x1, y1, image=arrivee, anchor='nw')

if __name__ == "__main__":
    app = VuePresentation()
    app.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        

