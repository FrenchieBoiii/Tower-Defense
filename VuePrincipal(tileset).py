import tkinter as tk 
from PIL import Image, ImageTk
from tkinter import scrolledtext,Canvas,PhotoImage

from Controleur import Controleur


class VuePresentation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("smooth attaque")
        self.geometry("700x300")
        self.resizable(False, False)
        
        self.creer_widgets()

    def creer_widgets(self):
        self.nom = tk.Label(self, text="Smooth attaque", bg='lightblue', font=("Algerian", 50))
        self.nom.pack(side=tk.TOP, fill='x')

        self.bouton_lancer_jeu = tk.Button(self, text="Lancer le jeu", font=("Calibri", 20), command=self.ouvrir_fenetre_jeu)
        self.bouton_lancer_jeu.pack(side=tk.TOP)

        self.bouton_quitter = tk.Button(self, text="Quitter l'application")
        self.bouton_quitter.bind("<Button-1>", self.quitter)
        self.bouton_quitter.pack(side=tk.BOTTOM)
    
    def quitter(self, event):
        self.destroy()

    def ouvrir_fenetre_jeu(self):
        fenetre_jeu = VuePrincipale(self, 1000, 700)
        fenetre_jeu.grab_set()


class VuePrincipale(tk.Toplevel):
    def __init__(self, parent, l_canvas=900, h_canvas=700,):        
        super().__init__(parent)
        self.title("Fenêtre de jeu")
        self.geometry(f"{l_canvas}x{h_canvas}")
        self.resizable(False, False)
        
        self.controleur = Controleur()
        self.grille = self.controleur.get_grille()

        
        self.taille_case = 20
        self.largeur = len(self.grille[0]) * self.taille_case
        self.hauteur = len(self.grille) * self.taille_case
        self.sprites = {} 
        self.load_all_sprites("images/pont.png", 1, 1, tile_size=20, prefix="wood_")
        self.load_all_sprites("images/tileset3.png", 4, 4, tile_size=20, prefix="tile3_")
        self.load_all_sprites("images/tileset.png", 7, 52, tile_size=16, prefix="ennemi_")
        self.creer_widgets()
        
        self.mode_placement = False


    def creer_widgets(self):
        
        frame_global = tk.Frame(self)
        frame_global.pack(fill="both", expand=True)
        
        #HAUT
        frame_haut = tk.Frame(frame_global)
        frame_haut.pack(side="top", fill="x", pady=5)
        
        self.label_defenses = tk.Label(frame_haut, text="Défenses : Tour d'archer, Tour de mage, Tour de baliste, Tour de feu, Muraille", font=("Arial", 12))
        self.label_defenses.pack(side="left", padx=10)
        
        frame_argent = tk.LabelFrame(frame_haut, text="Argent :", font=("Arial", 12, "bold"), fg="green")
        frame_argent.pack(side="right", padx=10)
        self.label_argent = tk.Label(frame_argent, text=str(self.controleur.get_argent()), font=("Arial", 16, "bold"), fg="green")
        self.label_argent.pack(padx=10, pady=5)

       
        #CENTRE
        frame_centre = tk.Frame(frame_global)
        frame_centre.pack(fill="both", expand=True)
    

        # Canvas (zone de jeu)
        self.canvas = tk.Canvas(frame_centre, width= self.largeur, height=self.hauteur, bg="white")
        self.canvas.pack(side="left", padx=10, pady=10)
        self.remplir_grille()
        # Lier le clic sur le canvas à la fonction de placement
        self.canvas.bind("<Button-1>", self.placer_defense)

        # Boutique à droite
        boutique = tk.Frame(frame_centre, width=300)
        boutique.pack(side="right", fill="y", padx=10, pady=10)

        label_boutique = tk.Label(boutique, text="Boutique", font=('Helvetica', 14, 'bold'))
        label_boutique.pack(pady=5)

        self.choix = tk.StringVar(value="Tour d'archer")


        tk.Radiobutton(boutique, text="Tour d'archer : 25 or", variable=self.choix, value="archer").pack(anchor="w")
        tk.Radiobutton(boutique, text="Tour de mage : 50 or", variable=self.choix, value="mage").pack(anchor="w")
        tk.Radiobutton(boutique, text="Tour de baliste : 75 or", variable=self.choix, value="baliste").pack(anchor="w")
        tk.Radiobutton(boutique, text="Tour de feu : 60 or", variable=self.choix, value="feu").pack(anchor="w")
        tk.Radiobutton(boutique, text="Muraille : 10 or", variable=self.choix, value="muraille").pack(anchor="w")


        bouton_accepter = tk.Button(boutique, text="Accepter", command=self.accepter_defense)
        bouton_accepter.pack(pady=10)

        # Zone d’aide
        self.aide = scrolledtext.ScrolledText(boutique, wrap=tk.WORD, width=30, height=10)
        self.aide.insert(tk.INSERT, "Bienvenue dans Smooth Attaque !\nChoisissez une défense à poser.")
        self.aide.pack(pady=10, fill="both", expand=True)

        #BAS
        frame_bas = tk.Frame(frame_global)
        frame_bas.pack(side="bottom", fill="x", pady=5)
        
        self.bouton_wave = tk.Button(frame_bas, text="Lancer la wave", command=self.lancer_wave)
        self.bouton_wave.pack(side="left", padx=10)
        
        self.label_wave = tk.Label(frame_bas, text="Wave 1", font=("Arial", 12, "bold"))
        self.label_wave.pack(side="left", padx=10)

        
        # Barre de vie
        tk.Label(frame_bas, text="HP :", font=("Arial", 12)).pack(side="left", padx=5)

        self.barre_vie = tk.Canvas(frame_bas, width=200, height=20, bg="gray")
        self.barre_vie.pack(side="left")
        self.maj_barre_vie()

        #Bouton fermer
        bouton_fermer = tk.Button(frame_bas, text="Fermer", command=self.destroy)
        bouton_fermer.pack(side="right", padx=10)
    
    
    def load_all_sprites(self, tileset_path, cols, rows, tile_size, prefix=""):
        tileset = Image.open(tileset_path)
        for y in range(rows):
            for x in range(cols):
                box = (x * tile_size, y * tile_size, (x + 1) * tile_size, (y + 1) * tile_size)
                sprite_img = tileset.crop(box)
                # Redimensionne à la taille de case utilisée
                sprite_img = sprite_img.resize((self.taille_case, self.taille_case), Image.Resampling.LANCZOS)
                key = f"{prefix}{x}_{y}"
                self.sprites[key] = ImageTk.PhotoImage(sprite_img)

    def accepter_defense(self):
        self.mode_placement = True

        self.aide.insert(tk.END, f"\nVous avez choisi : {self.choix.get()}\nCliquez sur le canvas pour placer.")
        self.aide.see(tk.END)
        
    def placer_defense(self, event):
        if self.mode_placement:
            # Calculer la position de la case cliquée
            col = event.x // self.taille_case
            row = event.y // self.taille_case
            type_def = self.choix.get()
            
            reussi, message = self.controleur.placer_defense(row, col, type_def)
            self.aide.insert(tk.END, f"\n{message}")
            self.aide.see(tk.END)
            
            if reussi:
                self.dessiner_defense(row, col, type_def)
                self.label_argent.config(text=str(self.controleur.get_argent()))
                self.mode_placement = False
        
    def dessiner_defense(self, row, col, type_def):
        x1 = col * self.taille_case
        y1 = row * self.taille_case
        x2 = x1 + self.taille_case
        y2 = y1 + self.taille_case

        if type_def == "archer":
            print("coucou")
            archer = self.sprites["tile3_1_3"]
            self.canvas.create_image(col*self.taille_case, row*self.taille_case, image=archer, anchor='nw')
            self.canvas.archer = archer
            #self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="black")
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
        self.canvas.delete("ennemi")  # Supprime les anciens dessins d'ennemis
        for ennemi in self.controleur.ennemis:
            row, col = ennemi.coord
            x1 = col * self.taille_case
            y1 = row * self.taille_case
            if ennemi.type_ennemi == "archer":
                archer = self.sprites["ennemi_0_16"]
                self.canvas.create_image(x1, y1, image=archer, anchor='nw', tags="ennemi")
                print("Sprite utilisé :", self.sprites["ennemi_0_16"])
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
    
    def lancer_tic(self):
        encore = self.controleur.prochain_tic()
        self.dessiner_ennemis()
        self.maj_barre_vie()
        self.label_argent.config(text=str(self.controleur.get_argent()))
        if encore:
            self.after(500, self.lancer_tic)
            
            
    def lancer_wave(self):
        self.controleur.demarrer_wave()
        self.label_wave.config(text=f"Wave {self.controleur.get_numero_wave()}")
        self.lancer_tic()


    def maj_barre_vie(self):
        self.barre_vie.delete("all")
        vie = self.controleur.get_vie()
        largeur = int((vie / 100) * 200)
        couleur = "green" if vie > 50 else "orange" if vie > 20 else "red"
        self.barre_vie.create_rectangle(0, 0, largeur, 20, fill=couleur)

    def remplir_grille(self):
        self.herbe_images = []
        self.montagnes_images = []
        self.riviere_images = []
        self.foret_images = []
        self.pont_images = []
        for row in range(len(self.grille)):
            for col in range(len(self.grille[row])):
                x1 = col * self.taille_case
                y1 = row * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case
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
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="pink", outline="")
                elif self.grille[row][col] == 'Arrivee':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="")

if __name__ == "__main__":
    app = VuePresentation()
    app.mainloop()

        

