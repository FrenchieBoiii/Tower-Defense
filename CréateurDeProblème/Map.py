import openpyxl

class Map():
    
    def __init__(self,fichier,feuille):
        
        self.map = self.get_excel_colors(fichier,feuille)
        
    
    def get_excel_colors(self,fichier,feuille):
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
                    
                    if couleur != 'FFC00000':
                        # Récupérer la couleur de fond de la cellule
                        
                        if fill and fill.fgColor and couleur:
                            color_row.append(couleur)
                        else:
                            color_row.append(None)  # Aucune couleur
                    else :
                        i = len(row)
                color_matrix.append(color_row)
                            
        wb.close()
        return color_matrix
    
    def affichage_map(self):
        for row in self.map:
            print(row)
            

            
