from algo import a_star
from mapp import visualize_grid,create_map
from tower import tower

ennemis = []
defenses = []

player_ready = False


rows, cols = 20, 30
money = 1000
vie = 100
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

def acheter_tour():
    nouvelle_defense = Defense()
    defenses.append(nouvelle_defense)
        
def debuter_jeu():
    create_map()
    derouler_jeu()
    
def derouler_jeu():
    niveau = 1
    while vie > 0:
        derouler_tour(niveau)
        niveau += 1
    fin_de_partie()

def phase_construction():
    pass
    
    
    
def derouler_tour(niveau):
    tic=0
    while not player_ready:
        phase_construction()
    while vie > 0 and ennemis != []:
        derouler_tic(niveau,tic)
        tic+=1
        
def derouler_tic(niveau,tic):
    spawn_ennemis(wave[niveau][tic])
    for ennemi in ennemis:
        ennemi.update()
    for defense in defenses:
        defense.update()
    ennemis = [ennemi for ennemi in ennemis if (ennemi.vivant or ennemi.arrivee)]
    
def fin_de_partie():
    pass
    

    
