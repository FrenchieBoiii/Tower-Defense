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
        """
        Fonction qui appelle la fonction tirer à une cadence voulue
        
        Entrées :
            ennemis : liste d'ennemis qui prennent des tirs
            dt : temps qui s'est écoulé depuis le dernier appel de la fonction update
        """
        self.timer += dt
        while self.timer >= self.cadence:
            self.tirer(ennemis)
            self.timer -= self.cadence
            self.cibles = []
        
        
    def tirer(self, ennemis):
        """
        Fonction qui enlève de la vie à certains ennemis dans la portée de la tour
        
        Entrées :
            ennemis : liste d'ennemis qui prennent des tirs
        """
        cibles = []
        for ennemi in ennemis:
            if self.dans_portee(ennemi.coord):
                cibles.append(ennemi)
        
        nb_ennemi_a_tuer = min(self.nb_ennemis_touches, len(cibles))
        for i in range(nb_ennemi_a_tuer):
            cibles[i].hp -= self.degats
        
            
    def dans_portee(self, pos_ennemi):
        """
        Fonction qui détecte si un ennemi est dans la portée de la tour
        
        Entrées :
            pos_ennemi : tuple indiquant la position d'un ennemi
        Sorties:
            dans_portee : booléen qui indique si l'ennemi est dans la portée de la tour
        """
        dx = pos_ennemi[0] - self.position[0]
        dy = pos_ennemi[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        dans_portee = distance <= self.distance_tir
        return dans_portee

class archer(Tour):
    def __init__(self, position):
        super().__init__(position, prix=25, cadence=1, degats=10, distance_tir=3, nb_ennemis_touches=1)


class mage(Tour):
    def __init__(self, position):
        super().__init__(position, prix=50, cadence=1.5, degats=25, distance_tir=4, nb_ennemis_touches=1)


class baliste(Tour):
    def __init__(self, position):
        super().__init__(position, prix=80, cadence=3.5, degats=40, distance_tir=4, nb_ennemis_touches=2)

class feu(Tour):
    def __init__(self, position):
        super().__init__(position, prix=60, cadence=1.5, degats=30, distance_tir=3, nb_ennemis_touches=2)


class muraille(Defense):
    def __init__(self, position):
        super().__init__(position, prix=10)
    def update(self, ennemis, dt):
        pass
        
        
        
        
        
        
