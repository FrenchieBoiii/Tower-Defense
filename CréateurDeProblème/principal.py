# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:42:45 2025

@author: jroussel
"""
import openpyxl
import tkinter as tk
from Mur import Mur
from Map import Map

class Jeu(tk.Tk):
    def __init__(self,fichier):
        
        self.fichier = fichier
        self.niveaux = self.création_des_niveaux()
        
        super().__init__()
        self.geometry("300x300")
        
        
    def création_des_niveaux(self):
        wb = openpyxl.load_workbook(self.fichier)
        i = 0
        dico = {}
        for sheet_name in wb.sheetnames:
            i += 1
            dico[i] = Map(self.fichier,sheet_name)                
        return dico
    
    def affichage_niveau_test(self,nb):
        return self.niveaux[nb].affichage_map()
        
    
                
jeu = Jeu("Map.xlsx")
jeu.affichage_niveau_test(1)
#jeu.mainloop()

