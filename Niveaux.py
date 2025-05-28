import openpyxl
from mapp import Mapp

class Niveaux(): #classe qui a partir d'un tableau excel va générer des maps
    def __init__(self,fichier_map):
        
        self.fichier_map =  fichier_map
        self.dico_mapps = self.création_des_mapps() #création du dico qui associe pour des numéros une map
        
        
    def création_des_mapps(self): 
        """
        Fonction qui creéer un dictionnaire avec en cléle numéro de wave et en valeur une map qui correspnd à une feuille du fichier excel.
    
        sorties : 
            dico : dictionnaire associant un numéro de wave avec une map
        """
        wb = openpyxl.load_workbook(self.fichier_map)
        i = 0
        dico = {}
        for sheet_name in wb.sheetnames:
            i += 1
            dico[i] = Mapp(self.fichier_map,sheet_name)                
        return dico
    
    def affichage_niveau_test(self,nb): 
        """
        Fonction qui affiche la carte associée à un niveau demandé
        
        Entrée :
            nb : entier, numéro de wave
        """
        return self.dico_mapps[nb].affichage_map()
    
    def niveau(self,nb): 
        """
        Fonction qui récupère la structure de la carte (mapp) pour le niveau demandé.
        
        Entrées :
            nb : entier, numéro du niveau
        """ 
        return self.dico_mapps[nb].mapp
                
