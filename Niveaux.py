import openpyxl
from mapp import Mapp

class Niveaux():
    def __init__(self,fichier_map):
        self.fichier_map =  fichier_map
        self.dico_mapps = self.création_des_mapps()
        
    def création_des_mapps(self): 
        """
        Fonction qui créer un dictionnaire avec en clé le numéro de wave et en valeur une map qui correspnd à une feuille du fichier excel.
        Sorties : 
            dico : dictionnaire associant un numéro de wave avec une map
        """
        wb = openpyxl.load_workbook(self.fichier_map)
        i = 0
        dico = {}
        for sheet_name in wb.sheetnames:
            i += 1
            dico[i] = Mapp(self.fichier_map,sheet_name)                
        return dico
    
    def niveau(self,nb): 
        """
        Fonction qui récupère la structure de la carte (mapp) pour le niveau demandé.
        
        Entrées :
            nb : entier, numéro du niveau
        """ 
        return self.dico_mapps[nb].mapp
                
