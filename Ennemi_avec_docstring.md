class Ennemi():
    
    def __init__(self,type_ennemi):
        
        self.vivant = True
        self.arrivée = False
        self.coor = ["",""]
        self.deplacement = []
        
        
        if type_ennemi == 'n' :
            self.hp = 10
            self.type = 'n'
        
        elif type_ennemi == 'b' :
            self.hp = 20
            self.type = 'b'
            
    def damage(self,nb):
    """
    fonction qui enlève à chaque ennemie les points de dégat 
        Entrees: nb, nombre de dégats, int
    """        
        self.hp -= nb
        if self.hp < 0 :
            self.vivant = False
        
    def deplacement(self):
    """
    fonction qui déplace les ennemies sur la map 
    """  
        self.coor = self.deplacement.pop(0)
        if len(self.deplacement) == 0 :
            self.arrivée = True
