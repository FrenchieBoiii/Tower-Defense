import openpyxl

class Mapp():
    
    def __init__(self,fichier_map,feuille):
        
        self.mapp = self.lecture_fichier_color(fichier_map,feuille)
        self.depart = self.trouver_coord("Depart")
        self.arrivee = self.trouver_coord("Arrivee")
        
    
    def lecture_fichier_color(self,fichier,feuille):
        # Ouvrir le fichier Excel
        wb = openpyxl.load_workbook(fichier)
        sheet = wb[feuille]
        
        color_matrix = []
        
        # Parcourir les cellules
        for row in sheet.iter_rows():
            color_row = []
            i = 0
            #print(row)
            fill0 = row[0].fill
            
            if fill0.fgColor.rgb == 'FFC00000':
                        
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
        coord = (0,0)
        for row_index, row in enumerate(self.mapp):
            for col_index, cell in enumerate(row):
                if cell == type_terrain:
                    coord = (row_index, col_index)
        return coord
