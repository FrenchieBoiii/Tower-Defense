
import tkinter as tk 
from PIL import Image, ImageTk
from tkinter import scrolledtext
#from ennemie import ennemie

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

#placer_tour
class VuePrincipale(tk.Toplevel):
    def __init__(self, parent, l_canvas=900, h_canvas=700,):        
        super().__init__(parent)
        self.title("Fenêtre de jeu")
        self.geometry(f"{l_canvas}x{h_canvas}")
        self.resizable(False, False)
        self.hp_total = 100
        self.hp_actuel = 100
        self.argent = tk.IntVar()
        #self.placer_tour = placer_tour
        self.argent.set(200)  # argent initial
        self.grille =[['Depart', 'Foret', 'Foret', 'Riviere', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Foret', 'Foret', 'Pont', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Foret', 'Foret', 'Riviere', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Montagne', 'Riviere', 'Riviere', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Montagne', 'Riviere', 'Chemin', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Montagne', 'Riviere', 'Chemin', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Montagne', 'Riviere', 'Chemin', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Montagne', 'Riviere', 'Riviere', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Chemin', 'Chemin', 'Pont', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Chemin', 'Chemin', 'Riviere', 'Chemin', 'Chemin'], 
                    ['Chemin', 'Chemin', 'Chemin', 'Riviere', 'Chemin', 'Arrivee']]
        self.taille_case = 50
        self.largeur = len(self.grille[0]) * self.taille_case
        self.hauteur = len(self.grille) * self.taille_case

        self.creer_widgets()

    def creer_widgets(self):
        
        frame_global = tk.Frame(self)
        frame_global.pack(fill="both", expand=True)
        
        #HAUT
        frame_haut = tk.Frame(frame_global)
        frame_haut.pack(side="top", fill="x", pady=5)
        
        self.label_defenses = tk.Label(frame_haut, text="Défenses : Tour, Mitraillette, Mur", font=("Arial", 12))
        self.label_defenses.pack(side="left", padx=10)
        
        frame_argent = tk.LabelFrame(frame_haut, text="Argent :", font=("Arial", 12, "bold"), fg="green")
        frame_argent.pack(side="right", padx=10)
        self.label_argent = tk.Label(frame_argent, textvariable=self.argent, font=("Arial", 16, "bold"), fg="green")
        self.label_argent.pack(padx=10, pady=5)

       
        #CENTRE
        frame_centre = tk.Frame(frame_global)
        frame_centre.pack(fill="both", expand=True)
    

        # Canvas (zone de jeu)
        self.canvas = tk.Canvas(frame_centre, width= self.largeur, height=self.hauteur, bg="white")
        self.canvas.pack(side="left", padx=10, pady=10)
        self.remplir_grille()

        # Boutique à droite
        boutique = tk.Frame(frame_centre, width=300)
        boutique.pack(side="right", fill="y", padx=10, pady=10)

        label_boutique = tk.Label(boutique, text="Boutique", font=('Helvetica', 14, 'bold'))
        label_boutique.pack(pady=5)

        self.choix = tk.StringVar(value="Tour")

        tk.Radiobutton(boutique, text="Tour : 100€", variable=self.choix, value="Tour").pack(anchor="w")
        tk.Radiobutton(boutique, text="Mitraillette : 50€", variable=self.choix, value="Mitraillette").pack(anchor="w")
        tk.Radiobutton(boutique, text="Mur : 10€", variable=self.choix, value="Mur").pack(anchor="w")

        bouton_accepter = tk.Button(boutique, text="Accepter", command=self.accepter_defense)
        bouton_accepter.pack(pady=10)

        # Zone d’aide
        self.aide = scrolledtext.ScrolledText(boutique, wrap=tk.WORD, width=30, height=10)
        self.aide.insert(tk.INSERT, "Bienvenue dans Smooth Attaque !\nChoisissez une défense à poser.")
        self.aide.pack(pady=10, fill="both", expand=True)

        #BAS
        frame_bas = tk.Frame(frame_global)
        frame_bas.pack(side="bottom", fill="x", pady=5)
        
        # Barre de vie
        tk.Label(frame_bas, text="HP :", font=("Arial", 12)).pack(side="left", padx=5)

        self.barre_vie = tk.Canvas(frame_bas, width=200, height=20, bg="gray")
        self.barre_vie.pack(side="left")
        self.maj_barre_vie()

        #Bouton fermer
        bouton_fermer = tk.Button(frame_bas, text="Fermer", command=self.destroy)
        bouton_fermer.pack(side="right", padx=10)

        # Lier le clic sur le canvas à la fonction de placement
        self.canvas.bind("<Button-1>", self.placer_tourelle)

    def accepter_defense(self):
        choix = self.choix.get()
        self.aide.insert(tk.END, f"\nVous avez choisi : {choix}")
        self.aide.see(tk.END)

        couts = {"Tour": 100, "Mitraillette": 50, "Mur": 10}
        cout = couts.get(choix, 0)
        if self.changer_argent(-cout):
            self.mode_placement = True  # Activer le mode de placement
            self.aide.insert(tk.END, "\nCliquez sur le canvas pour placer votre défense.")
            self.aide.see(tk.END)
        

        
    def maj_barre_vie(self):
        self.barre_vie.delete("all")
        largeur = int((self.hp_actuel / self.hp_total) * 200)
        couleur = "green" if self.hp_actuel > 50 else "orange" if self.hp_actuel > 20 else "red"
        self.barre_vie.create_rectangle(0, 0, largeur, 20, fill=couleur)
        
        
    def diminuer_hp(self, montant):  #=> à appeler lorsque les vies baissent 
        self.hp_actuel = max(0, self.hp_actuel - montant)
        self.maj_barre_vie()
        
    def changer_argent(self, montant):
        nouveau_montant = self.argent.get() + montant
        if nouveau_montant < 0:
            #prévenir le joueur que c'est pas possible
            self.aide.insert(tk.END, "\nPas assez d'argent !")
            self.aide.see(tk.END)
            return
        self.argent.set(nouveau_montant)
        return True  # Retourner True si l'argent a été changé avec succès
    
    def placer_tourelle(self, event):
        if not self.mode_placement:
            return  # Ne rien faire si on n'est pas en mode placement

        # Calculer la position de la case cliquée
        col = event.x // self.taille_case
        row = event.y // self.taille_case
        self.placer_tour((row, col), self.choix.get())  # Appeler la fonction de placement de tourelle
        # Vérifier si la case est valide pour placer une tourelle
        if self.grille[row][col] == 'Foret' or self.grille[row][col] == 'Riviere' or self.grille[row][col] == 'Montagne':
            self.aide.insert(tk.END, "\nVous ne pouvez pas placer une tourelle ici.")
            self.aide.see(tk.END)
            return

        # Placer la tourelle sur le canvas
        x1 = col * self.taille_case
        y1 = row * self.taille_case
        x2 = x1 + self.taille_case
        y2 = y1 + self.taille_case
        if self.choix.get() == "Tour":
            self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="black")
        elif self.choix.get() == "Mitraillette":
            self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="black")
        elif self.choix.get() == "Mur":
            self.canvas.create_rectangle(x1, y1, x2, y2-25, fill="gray", outline="black")
        self.aide.insert(tk.END, f"\nTourelle placée en ({row}, {col}).")
        self.aide.see(tk.END)

        # Désactiver le mode de placement
        self.mode_placement = False

    def remplir_grille(self):

        # Dessin de la grille
        for i in range(0, self.largeur, self.taille_case):
            self.canvas.create_line(i, 0, i, self.hauteur, fill="black")
        for j in range(0, self.hauteur, self.taille_case):
            self.canvas.create_line(0, j, self.largeur, j, fill="black")

        for row in range(len(self.grille)):
            for col in range(len(self.grille[row])):
                x1 = col * self.taille_case
                y1 = row * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="beige", outline="")
                if self.grille[row][col] == 'Montagne':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgrey", outline="")
                elif self.grille[row][col] == 'Riviere':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="")
                elif self.grille[row][col] == 'Foret':
                    self.canvas.create_oval(x1, y1, x2, y2, fill="dark green", outline="")
                elif self.grille[row][col] == 'Pont':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="brown", outline="")
                elif self.grille[row][col] == 'Depart':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="pink", outline="")
                elif self.grille[row][col] == 'Arrivee':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="")

        # Dessin de la grille
        for i in range(0, self.largeur, self.taille_case):
            self.canvas.create_line(i, 0, i, self.hauteur, fill="grey")
        for j in range(0, self.hauteur, self.taille_case):
            self.canvas.create_line(0, j, self.largeur, j, fill="grey")

if __name__ == "__main__":
    app = VuePresentation()
    app.mainloop()

        
        
app = VuePrincipale()
app.mainloop()
