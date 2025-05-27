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
        self.hp -= nb
        if self.hp < 0 :
            self.vivant = False

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
