import openpyxl


def lecture_fichier_wave(fichier,feuille=None): #renvoie un dico qui pour chaque wave sous forme de numéro lui associe une liste qui représente chaque tic de la manche
    
    wb = openpyxl.load_workbook(fichier)
    
    if feuille is None:
        sheet = wb.active
    else:
        sheet = wb[feuille]

    
    wave_ennemi_dico = {}
    liste = []
    str_ennemi = ''
    ennemi_type =''
    i = 0
    for row in sheet.iter_rows(values_only=True):
        val_0 = str(row[0])
        i = 0
        if val_0[:4] != "wave" :
            while i < len(row) and row[i] != None :
                valeur = str(row[i])
                if valeur != '0':
                    if i == 0:
                        ennemi_type = 'paysan'
                    elif i == 1:
                        ennemi_type = 'bandit'
                    elif i == 1:
                        ennemi_type = 'archer'
                    elif i == 1:
                        ennemi_type = 'chevalier'
                    elif i == 1:
                        ennemi_type = 'catapulte'
                    elif i == 1:
                        ennemi_type = 'seigneur'
                    str_ennemi += ennemi_type
                i += 1
            
            liste.append(str_ennemi)
            str_ennemi = ''
            
        else :
            wave_ennemi_dico[row[0][4:]] = liste
            liste = []
    return wave_ennemi_dico
