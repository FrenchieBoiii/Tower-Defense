class Ennemi():
    
    def __init__(self,type_ennemi):
        
        self.vivant = True
        self.arrivee = False
        self.coord = ["",""]
        self.deplacement = []
        self.distance_parcourue = 0
        self.type_ennemi = type_ennemi
        
        
        if type_ennemi == 'paysan' :
            self.hp = 30
            self.degats = 1
            self.recompense = 5
        
        elif type_ennemi == 'bandit' :
            self.hp = 50
            self.degats = 2
            self.recompense = 8
        elif type_ennemi == 'archer' :
            self.hp = 40
            self.degats = 2
            self.recompense = 10
        elif type_ennemi == 'chevalier' :
            self.hp = 100
            self.degats = 4
            self.recompense = 15
        elif type_ennemi == 'catapulte' :
            self.hp = 80
            self.degats = 10
            self.recompense = 20
        elif type_ennemi == 'seigneur' :
            self.hp = 300
            self.degats = 15
            self.recompense = 50

            
    def damage(self,nb):
        """
        fonction qui enlève à chaque ennemie les points de dégat et met à jour la variable vivant de l'ennemi'
            Entrees: nb, nombre de dégats, int
        """    
        self.hp -= nb
        if self.hp < 0 :
            self.vivant = False

    def update(self):
        """
        fonction qui déplace les ennemies sur la map et met à jour leurs positions 
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
