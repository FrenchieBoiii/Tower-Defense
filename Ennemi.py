# -*- coding: utf-8 -*-
"""
Created on Wed May  7 14:35:05 2025

@author: jerem
"""

class Ennemi():
    
    def __init__(self,type_ennemi):
        
        self.vivant = True
        self.arrivee = False
        self.coord = ["",""]
        self.deplacement = []
        self.distance_parcourue = 0
        self.type_ennemi = type_ennemi
        self.degats = 10
        
        
        if type_ennemi == 'n' :
            self.hp = 10
        
        elif type_ennemi == 'b' :
            self.hp = 20
            
    def damage(self,nb):
        self.hp -= nb
        if self.hp < 0 :
            self.vivant = False
            """
    def deplacer(self):
        self.coord = self.deplacement.pop(0)
        print(self.coord)
        self.distance_parcourue += 1
        if len(self.deplacement) == 0 :
            #print("ennemi arrivee")
            self.arrivee = True
          """  
    def update(self):
        if self.hp <= 0:
            self.vivant = False
        if self.deplacement:
            self.coord = self.deplacement.pop(0)
            self.distance_parcourue += 1
            if len(self.deplacement) == 0:
                self.arrivee = True
        else:
            print("ennemi bloqué")

        