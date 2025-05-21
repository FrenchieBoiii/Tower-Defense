from algo import a_star
from mapp import visualize_grid,create_map
from tower import tower
from Niveaux import Niveaux
from Ennemi import Ennemi

jeu = Niveaux("Map.xlsx","Wave.xlsx")
dico_niveaux = jeu.création_des_niveaux()

ennemis = []
defenses = []

argent = 1000
vie = 100

player_ready = False



def acheter_tour():
    """
    fonction qui ajoute à la liste des défences la défense choisie
    """
    nouvelle_defense = Defense()
    defenses.append(nouvelle_defense)
        
def debuter_jeu():
    """
    fonction qui récupère le niveau choisi par l'utilisateur et appel la fonction dérouler_jeu avec le niveau choisi
    """
    niveaux = Niveaux()
    derouler_jeu(niveaux)
    
def derouler_jeu(niveaux):
    """
    fonction qui lance une game à partir d'un certain niveau, arrête la partie lorsqu'il n'y a pas de vie
        Entrees: niveaux, liste des niveaux
    """
    niveau = 0
    
    while vie > 0:
        mapp = niveaux[niveau].mapp
        wave = niveaux[niveau].wave
        derouler_tour(niveau, mapp, wave)
        niveau += 1
        
    fin_de_partie()

def phase_construction(mapp):
    pass
    
def spawn_ennemi(type_ennemi):
    """
    fonction ajoute un type d'annemie à la liste des ennemies de la vague d'annemies
        Entrees: type d'ennemie, int
    """
    nouveau_ennemi = Ennemi(type_ennemi)
    ennemis.append(nouveau_ennemi)
    
    
def derouler_tour(niveau, mapp, wave):
    """
    fonction qui fait dérouler le jeu tant qu'il y a des vies
        Entrees: niveau, int
                mapp, map
                wave, liste d'ennemie
    """
    tic=0
    while not player_ready:
        phase_construction(mapp)
    while vie > 0 and ennemis != []:
        derouler_tic(niveau,tic, mapp, wave)
        tic+=1
        
def derouler_tic(niveau,tic, mapp, wave):
    """
    fonction qui pour un tic met à jour la map
        Entrees: niveau, int
                tic, int
                mapp, map
                wave, liste d'ennemies
    """
    spawn_ennemi(wave[str(niveau+1)][tic])
    for ennemi in ennemis:
        ennemi.deplacement()
    for defense in defenses:
        defense.update()
    ennemis[:] = [e for e in ennemis if e.vivant and not e.arrivee]
    
def fin_de_partie():
    """
    fonction qui affcihe un message en fin de partie 
    """
    print("Vous n'avez plus de vie. Vous avez perdu.")
