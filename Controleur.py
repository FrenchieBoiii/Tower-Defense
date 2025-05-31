import tower
from Ennemi import Ennemi
from Niveaux import Niveaux
import algo
import time
import creation_wave

class Controleur:
    def __init__(self):
        self.niveaux = Niveaux("Map.xlsx")
        self.mapp = self.niveaux.dico_mapps[1]  # une seule map
        self.grille = self.mapp.mapp
        self.wave_data = creation_wave.lecture_fichier_wave("Wave.xlsx")

        self.depart = self.mapp.depart
        self.arrivee = self.mapp.arrivee
        
        self.ennemis = []
        self.defenses = []
        self.vie = 100
        self.argent = 100
        self.tic = 0
        self.sang = []
        
        self.numero_wave = 1
        self.wave_en_cours = False
        self.player_ready = False
        
        self.dernier_temps = time.time()
        

    def peut_placer(self, row, col):
        """
        Vérifie si une défense peut être placée sur une case de la grille.

        Entrées :
            row: entier, ligne de la case
            col: entier, colonne de la case

        Sorties :
            peut_placer: booléen indiquant si le placement est possible
        """
        peut_placer = True
        grille_temp = [r.copy() for r in self.grille]
        grille_temp[row][col] = "Mur"

        if self.grille[row][col] in ["Foret", "Riviere", "Montagne"]:
            peut_placer = False
        elif algo.chemin_bloque(grille_temp, self.depart, self.arrivee):
            peut_placer = False
        return peut_placer
        

    def placer_defense(self, row, col, type_def):
        """
        Tente de placer une défense du type donné sur une case donnée de la grille.

        Entrées :
            row: entier, ligne de la grille
            col: entier, colonne de la grille
            type_def: string indiquant le type de défense ("archer", "mage", "baliste", "feu", "muraille")

        Sorties :
             peut_placer: booléen indiquant la réussite
             reponse: string du message associé pour l'utilisateur
        """
        peut_placer = True
        reponse = f"\n Tour de {type_def} placée en ({row}, {col}). Placez une nouvelle défense ou lancer la wave."
        if self.peut_placer(row, col):
            if type_def == "archer":
                nouvelle_defense = tower.archer(position=(row, col)) 
            elif type_def == "mage":
                nouvelle_defense = tower.mage(position=(row, col))
            elif type_def == "baliste":
                nouvelle_defense = tower.baliste(position=(row, col))
            elif type_def == "feu":
                nouvelle_defense = tower.feu(position=(row, col))
            elif type_def == "muraille":
                nouvelle_defense = tower.muraille(position=(row, col))
            
            if nouvelle_defense.prix > self.argent:
                peut_placer = False
                reponse = "Pas assez d'argent."
            else:
                self.argent -= nouvelle_defense.prix
                self.grille[row][col] = "Mur"
                self.defenses.append(nouvelle_defense)
                
        else:
            peut_placer = False
            reponse = "Terrain invalide pour une défense. Placez la défense à un autre endroit."
            
        return peut_placer, reponse


    def spawn_ennemi(self, type_ennemi):
        """
        Fait apparaître un ennemi au point de départ et lui attribue son chemin.

        Entrée :
            type_ennemi : string représentant le type de l'ennemi
        """
        ennemi = Ennemi(type_ennemi)
        ennemi.coord = self.depart 
        ennemi.deplacement = self.chemin_ennemis[1:]
        if len(type_ennemi) >1:
            self.ennemis.append(ennemi)
        
    def demarrer_wave(self):
        """
        Démarre une nouvelle vague d'ennemis en initialisant le chemin à suivre
        et réinitialisant le compteur de tic.
        """
        self.wave_en_cours = True
        self.tic = 0
        self.chemin_ennemis = algo.trouver_chemin(self.grille, self.mapp.depart, self.mapp.arrivee)
        

    def prochain_tic(self):
        """
        Gère les événements d'un tic de jeu pendant une vague :
        - Fait apparaître de nouveaux ennemis si c'est le bon moment
        - Avance les ennemis existants
        - Termine la vague si plus d'ennemis

        Sortie :
            reste_ennemis : booléen indiquant si la vague est encore en cours ou pas
        """
        self.mettre_a_jour_jeu()
        
        if self.wave_en_cours and not self.est_game_over() and not self.a_gagne():
            wave = self.wave_data[str(self.numero_wave)]
            reste_ennemis = True
            
            depart_libre = True
            for ennemi in self.ennemis:
                if ennemi.coord == self.depart:
                    depart_libre = False
            
            if self.tic < len(wave) and depart_libre:
                self.spawn_ennemi(wave[self.tic])
                self.tic += 1

            elif len(self.ennemis) == 0:
                self.wave_en_cours = False
                self.numero_wave += 1
                reste_ennemis = False
            else:
                self.tic += 1

            return reste_ennemis

    def mettre_a_jour_jeu(self):
        """
        Met à jour tous les éléments du jeu :
        - Déplace les ennemis
        - Gère les morts (récompenses, taches de sang)
        - Applique les dégâts si un ennemi atteint l'arrivée
        - Met à jour les défenses (tire)
        """
        maintenant = time.time()
        dt = maintenant - self.dernier_temps
        self.dernier_temps = maintenant
        
        for ennemi in self.ennemis:
            ennemi.update()
            if ennemi.arrivee:
                self.diminuer_vie(ennemi.degats)  
                ennemi.vivant = False
                self.ennemis.remove(ennemi)
            elif not ennemi.vivant:
                self.sang.append(ennemi.coord)
                self.argent += ennemi.recompense
                self.ennemis.remove(ennemi)
        for defense in self.defenses:
            defense.update(self.ennemis, dt)

    def diminuer_vie(self, quantite):
        """
        Diminue la vie du joueur d'une certaine quantité (sans aller en dessous de 0).

        Entrée :
            quantite : entier indiquant le nombre de points de vie à retirer

        Sortie :
            vie: entier indiquant la vie restante du joueur
        """
        self.vie = max(0, self.vie - quantite)
        return self.vie

    def est_game_over(self):
        """
        Vérifie si le joueur a perdu la partie.

        Retour :
           game_over : booléen indiquant si la vie est à 0 ou moins 
        """
        return self.vie <= 0
    
    def a_gagne(self):
        """
        Vérifie si le joueur a gagné la partie.

        La victoire est déterminée par l'absence de nouvelles vagues à lancer
        dans les données du fichier de vagues.

        Sortie :
            a_gagne : booléen indiquant si toutes les vagues ont été terminées
        """
        a_gagne= False
        if str(self.numero_wave) not in self.wave_data:
            a_gagne = True
        return a_gagne
        
    def wave_terminee(self):
        """
        Réinitialise les effets visuels liés à la vague terminée (ex. taches de sang).
        """
        self.sang = []















