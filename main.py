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

"""
rows, cols = 20, 30

coord_spawn = (rows/2,0)
coord_arrivee = (rows/2,cols-1)

grid = create_map(rows,cols)
#grid = [[1, 1, 1, 1, 1],[1, 100, 100, 100, 1],[1, 1, 1, 1, 1],[1, 100, 100, 100, 1],[1, 1, 1, 1, 1]]

print("Initial Grid:")
visualize_grid(grid)
    
start = (0, 0)  # Starting point (top-left corner)
goal = (19, 29)  # Goal point (bottom-right corner)

# Find the path using A* algorithm
path = a_star(grid, start, goal)

# Visualize the grid with the path
if path != []:
    print("Path found:")
    visualize_grid(grid, path)
else:
    print("No path found.")

"""

def acheter_tour():
    nouvelle_defense = Defense()
    defenses.append(nouvelle_defense)
        
def debuter_jeu():
    niveaux = Niveaux()
    derouler_jeu(niveaux)
    
def derouler_jeu(niveaux):
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
    nouveau_ennemi = Ennemi(type_ennemi)
    ennemis.append(nouveau_ennemi)
    
    
def derouler_tour(niveau, mapp, wave):
    tic=0
    while not player_ready:
        phase_construction(mapp)
    while vie > 0 and ennemis != []:
        derouler_tic(niveau,tic, mapp, wave)
        tic+=1
        
def derouler_tic(niveau,tic, mapp, wave):
    spawn_ennemi(wave[str(niveau+1)][tic])
    for ennemi in ennemis:
        ennemi.deplacement()
    for defense in defenses:
        defense.update()
    ennemis[:] = [e for e in ennemis if e.vivant and not e.arrivee]
    
def fin_de_partie():
    print("Vous n'avez plus de vie. Vous avez perdu.")
    
    
    
