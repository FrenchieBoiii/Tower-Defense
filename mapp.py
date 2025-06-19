import openpyxl

class Mapp():
    
    def __init__(self,fichier_map,feuille):
        
        self.mapp = self.lecture_fichier_color(fichier_map,feuille)
        self.depart = self.trouver_coord("Depart")
        self.arrivee = self.trouver_coord("Arrivee")
        
    
    def lecture_fichier_color(self,fichier,feuille):
        """
        Fonction qui créer la map en couleur à partir de l'excel et de la feuille choisie
        Interprètation des cellules de la feuille excel 
        
        Entrées :
            Fichier : string du chemin vers le fichier excel
            feuille : string du numéro de la feuille du fichier excel correspondant à la map voulue
        Sorties :
            color_matrix : liste 2D, matrice représentant la map utilisée pour le jeu
        """
        wb = openpyxl.load_workbook(fichier) #Avec Chat GPT
        sheet = wb[feuille]
        
        color_matrix = []
        
        for row in sheet.iter_rows():
            color_row = []
            i = 0
            fill0 = row[0].fill
            if fill0.fgColor.rgb == 'FFC00000': #Fin de Chat GPT
                wb.close()
                return color_matrix
            else:
                while i != len(row):
                    cell = row[i]
                    i +=1
                    fill = cell.fill
                    couleur = fill.fgColor.rgb 
                    if couleur == 'FFFFFFFF' or couleur == '00000000':
                        color_row.append('Chemin')
            
                    elif couleur == 'FFC00000':
                        i = len(row)  
                    
                    elif couleur == 'FF4D4D4D':
                        color_row.append('Montagne')
                        
                    elif couleur == 'FF0066FF':
                        color_row.append('Riviere')
                        
                    elif couleur == 'FF006600':
                        color_row.append('Foret')
                    
                    elif couleur == 'FF996633':
                        color_row.append('Pont')
                        
                    elif couleur == 'FFD60093':
                        color_row.append('Depart')
                        
                    elif couleur == 'FFFF3300':
                        color_row.append('Arrivee')
                    else :
                        color_row.append(couleur)
                        
                color_matrix.append(color_row)

    def trouver_coord(self, type_terrain):
        """
        Fonction qui cherche les coordonnées de la dernière occurence d'un type de terrain voulue sur la map
        
        Entrée :
            Type_terrain  : string du nom du terrain qu'on recherche
        Sortie : 
            coord : tuple indiquant les coordonées de la dernière cellule du terrain voule qui a été trouvé
        """
        coord = (0, 0)
        row_index = 0
        for row in self.mapp:
            col_index = 0
            for cell in row:
                if cell == type_terrain:
                    coord = (row_index, col_index)
                col_index += 1
            row_index += 1
        return coord
