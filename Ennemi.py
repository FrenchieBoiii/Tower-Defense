
class Ennemi():
    
    def __init__(self,type_ennemi, multiplier_hp):
        
        self.vivant = True
        self.arrivee = False
        self.coord = ["",""]
        self.deplacement = []
        self.distance_parcourue = 0
        self.type_ennemi = type_ennemi
        
        
        if type_ennemi == 'paysan' :
            self.hp = 40*multiplier_hp
            self.degats = 1
            self.recompense = 3
        
        elif type_ennemi == 'bandit' :
            self.hp = 70*multiplier_hp
            self.degats = 2
            self.recompense = 6
        elif type_ennemi == 'archer' :
            self.hp = 50*multiplier_hp
            self.degats = 4
            self.recompense = 8
        elif type_ennemi == 'chevalier' :
            self.hp = 150*multiplier_hp
            self.degats = 6
            self.recompense = 10
        elif type_ennemi == 'catapulte' :
            self.hp = 120*  multiplier_hp
            self.degats = 12
            self.recompense = 15
        elif type_ennemi == 'seigneur' :
            self.hp = 500*  multiplier_hp
            self.degats = 40
            self.recompense = 50

            
    def damage(self,nb):
        """
        fonction qui enlève à chaque ennemie les points de dégat et met à jour la variable vivant de l'ennemi
            Entrées: 
                nb: int qui indique les dégats reçus
        """    
        self.hp -= nb
        if self.hp < 0 :
            self.vivant = False

    def update(self):
        """
        fonction qui déplace les ennemies sur la map, met à jour leurs positions et détecte s'ils sont arrivés
        """  
        if self.hp <= 0:
            self.vivant = False
            
        if self.deplacement:
            self.coord = self.deplacement.pop(0)
            self.distance_parcourue += 1
            if len(self.deplacement) == 0:
                self.arrivee = True
        else:
            print("ennemi bloqué")
