

Classe défense : 

créer les objets défensifs avec leur position
=> sous classes par type de défense : cadence de tirs, dégâts, distance de tir, nombre d’ennemis touchés et coût

fonction : 
acheter_défense : réduit argent et positionne la tour
placer_defense : permet d’ajouter la défense sur le curseur de la souris
tirer : vérifie si il y un ou des ennemis dans son périmètre et lui enlève des vies



class Defense:
    def __init__(self,position,prix):
        position = self.position
        prix = self.prix
    
    def placer_defense(self,coord,type_de_tour):
        tour_placee = False
        grid_a_tester = mapp.ajouter_tour(coord,type_de_tour)
        if !chemin_bloque(grid_a_tester):
            grid = grid_a_tester
        
        return tour_placee   #false si tour ne peut pas etre placee
        
class Tour(Defense):
    def __init__(self,cadence,degats,distance_tir,nb_ennemies_touches):
        super().__init__()
        cadence = self.cadence
        degats = self.degats
        distance_tir = self.distance_tir
        nb_ennemies_touches = self.nb_ennemies_touches
    
    def tirer(self,ennemi):
        for ennemi in ennemis:
            if ennemi in distance:
                baisser vie ennemi
    
    
class Mur(Defense):
    