
import algo
import math


class Defense:
    def __init__(self,position,prix):
        self.position = position
        self.prix = prix

        
class Tour(Defense):
    def __init__(self, position, prix, cadence, degats, distance_tir, nb_ennemis_touches):
        super().__init__(position, prix)
        self.cadence = cadence
        self.degats = degats
        self.distance_tir = distance_tir
        self.nb_ennemis_touches = nb_ennemis_touches
        self.timer = 0

    def update(self, ennemis, dt):
        self.timer += dt
        intervalle_tir = 1 / self.cadence
        while self.timer >= intervalle_tir:
            self.tirer(ennemis)
            self.timer -= intervalle_tir
        
        
    def tirer(self, ennemis):
        cibles = []
        for ennemi in ennemis:
            if self.dans_portee(ennemi.coord):
                cibles.append(ennemi)
        
        #cibles = sorted(cibles, key=lambda e: e.distance_parcourue)

        
        nb_ennemi_a_tuer = min(self.nb_ennemis_touches, len(cibles))
        for i in range(nb_ennemi_a_tuer):
            cibles[i].hp -= self.degats
            
    def dans_portee(self, pos_ennemi):
        dx = pos_ennemi[0] - self.position[0]
        dy = pos_ennemi[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        dans_portee = distance <= self.distance_tir
        return dans_portee

class archer(Tour):
    def __init__(self, position):
        super().__init__(position, prix=25, cadence=0.7, degats=15, distance_tir=3, nb_ennemis_touches=1)


class mage(Tour):
    def __init__(self, position):
        super().__init__(position, prix=50, cadence=1, degats=30, distance_tir=4, nb_ennemis_touches=2)


class baliste(Tour):
    def __init__(self, position):
        super().__init__(position, prix=75, cadence=2.5, degats=60, distance_tir=5, nb_ennemis_touches=3)

class feu(Tour):
    def __init__(self, position):
        super().__init__(position, prix=60, cadence=1, degats=30, distance_tir=3, nb_ennemis_touches=2)


class Mur(Defense):
    def __init__(self, position):
        super().__init__(position, prix=10)
    def update(self, ennemis, dt):
        pass
        
        
        
