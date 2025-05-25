import tower
from Ennemi import Ennemi
from Niveaux import Niveaux
import algo
import time
import creation_wave

class Controleur:
    def __init__(self):
        self.niveaux = Niveaux("Map.xlsx")
        self.mapp = self.niveaux.dico_mapps[3]  # une seule map
        self.grille = self.mapp.mapp
        self.wave_data = creation_wave.lecture_fichier_wave("Wave.xlsx")

        self.depart = self.mapp.depart
        self.arrivee = self.mapp.arrivee
        #print(f"depart : {self.depart} et arrivee : {self.arrivee}")
        
        self.ennemis = []
        self.defenses = []
        self.vie = 100
        self.argent = 200
        self.tic = 0
        
        self.numero_wave = 1
        self.wave_en_cours = False
        self.player_ready = False
        
        self.dernier_temps = time.time()
        
    def get_argent(self):
        return self.argent

    def get_vie(self):
        return self.vie

    def get_grille(self):
        return self.grille
    def get_numero_wave(self):
        return self.numero_wave
    
    def peut_placer(self, row, col):
        peut_placer = True
        grille_temp = [r.copy() for r in self.grille]
        grille_temp[row][col] = "Mur"

        if self.grille[row][col] in ["Foret", "Riviere", "Montagne"]:
            peut_placer = False
        elif algo.chemin_bloque(grille_temp, self.depart, self.arrivee):
            peut_placer = False
        return peut_placer
        

    def placer_defense(self, row, col, type_def):
        if not self.peut_placer(row, col):
            return False, "Terrain invalide pour une défense."

        couts = {"Tour": 100, "Mitraillette": 50, "Mur": 10}
        cout = couts.get(type_def, 0)
        if self.argent < cout:
            return False, "Pas assez d'argent."

        self.argent -= cout
        self.grille[row][col] = "Mur"
        
        if type_def == "Tour":
            nouvelle_defense = tower.Archer(position=(row, col)) 
        elif type_def == "Mitraillette":
            nouvelle_defense = tower.Mitraillette(position=(row, col))
        elif type_def == "Mortier":
            nouvelle_defense = tower.Mortier(position=(row, col))
        elif type_def == "Mur":
            nouvelle_defense = tower.Mur(position=(row, col))

            
        self.defenses.append(nouvelle_defense)
        return True, f"{type_def} placée en ({row}, {col})."


    def spawn_ennemi(self, type_ennemi):
        ennemi = Ennemi(type_ennemi)
        ennemi.coord = self.depart 
        ennemi.deplacement = self.chemin_ennemis[1:]
        self.ennemis.append(ennemi)
        
        
    def demarrer_wave(self):
        self.wave_en_cours = True
        self.tic = 0
        self.chemin_ennemis = algo.trouver_chemin(self.grille, self.mapp.depart, self.mapp.arrivee)
        

    def prochain_tic(self):
        self.mettre_a_jour_jeu()
        
        if self.wave_en_cours and not self.est_game_over():
            wave_str = str(self.numero_wave)
            if wave_str in self.wave_data:
                wave = self.wave_data[wave_str]
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
        maintenant = time.time()
        dt = maintenant - self.dernier_temps
        self.dernier_temps = maintenant
        
        for ennemi in self.ennemis:
            ennemi.update()
            if ennemi.arrivee:
                self.diminuer_vie(ennemi.degats)  
                ennemi.vivant = False
        for defense in self.defenses:
            defense.update(self.ennemis, dt)
        self.ennemis = [e for e in self.ennemis if e.vivant and not e.arrivee]

    def diminuer_vie(self, quantite):
        self.vie = max(0, self.vie - quantite)
        return self.vie

    def est_game_over(self):
        return self.vie <= 0

    def wave_terminee(self):
        current_wave = self.wave_data.get(str(self.wave_index), [])
        return self.tic >= len(current_wave) and len(self.ennemis) == 0

    def fin_de_partie(self):
        print("Vous n'avez plus de vie. Vous avez perdu.")


























