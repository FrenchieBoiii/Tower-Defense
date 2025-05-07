# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:42:45 2025

@author: jroussel
"""
import openpyxl
from mapp import Mapp

class Niveaux(): #classe qui a partir d'un tableau excel va générer des maps
    def __init__(self,fichier_map,fichier_wave):
        
        self.fichier_map =  fichier_map
        self.fichier_wave = fichier_wave
        
    def création_des_niveaux(self): #pour chaque feuille du fichier, on va créer un objet map
        wb = openpyxl.load_workbook(self.fichier_map)
        i = 0
        dico = {}
        for sheet_name in wb.sheetnames:
            i += 1
            dico[i] = Mapp(self.fichier_map,self.fichier_wave,sheet_name)                
        return dico
    
    def affichage_niveau_test(self,nb): #fonction pour afficher une map dans l'invit de commande
        return self.dico_niveaux[nb].affichage_map()
    
    def niveau(self,nb): #fonction pour récupérer
        return self.dico_niveaux[nb].map
    
    
