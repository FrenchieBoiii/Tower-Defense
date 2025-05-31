import heapq

def manhattan_distance(start, end):
    """
    fonction qui définie la distance Manhattan, distance entre 2 points avec des déplacment horizontaux et verticaux
        Entrées:
            start: tuple indiquant les coordonnées du point de départ
        Sorties: 
            distance Manhattan: int indiquant la distance manhattan
    """    
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def a_star(grid, start, goal):
    """
    fonction qui trouve le chemin le plus court entre deux points sur une grille en utilisant l'algorithme A*
        Entrées:
            grid: liste 2D de la map
            start: tuple indiquant les coordonées du point de départ
            goal: tuple indiquant les coordonées du point d'arrivé
        Sorties: 
            path : Liste de coordonnées 2D représentant le chemin trouvé du point de départ au point d'arrivée
    """  
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    g_costs = [[float('inf')] * cols for i in range(rows)]
    g_costs[start[0]][start[1]] = 0

    f_costs = [[float('inf')] * cols for i in range(rows)]
    f_costs[start[0]][start[1]] = manhattan_distance(start, goal)

    open_list = []
    heapq.heappush(open_list, (f_costs[start[0]][start[1]], start))

    came_from = {}
    path = []
    continuer = True
    
    while open_list and continuer:
        current_f_cost, current = heapq.heappop(open_list)
        x, y = current

        if current == goal:
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            continuer = False
        
        if continuer:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
    
                if 0 <= nx < rows and 0 <= ny < cols:
                    if grid[nx][ny] == float('inf'):
                        continue
    
                    move_cost = grid[nx][ny]
                    tentative_g_cost = g_costs[x][y] + move_cost
    
                    if tentative_g_cost < g_costs[nx][ny]:
                        g_costs[nx][ny] = tentative_g_cost
                        f_cost = tentative_g_cost + manhattan_distance((nx, ny), goal)
                        f_costs[nx][ny] = f_cost
    
                        heapq.heappush(open_list, (f_cost, (nx, ny)))
                        came_from[(nx, ny)] = (x, y)
    return path


def str_vers_int(grille):
    """
    Fonction qui converti une grille de chaînes de caractères en une grille d'entiers.

    Les cellules contenant les chaînes "Chemin", "Pont", "Depart" ou "Arrivee" sont converties en 1.
    Les autres cellules sont converties en float('inf').

    Entrées :
        grille : liste 2D avec des string
    
    Sorties : 
        grille_int : liste 2D avec des entiers
    """
    grille_int = []
    for row in grille:
        row_int = []
        for cell in row:
            if cell in ["Chemin", "Pont", "Depart", "Arrivee"]:
                row_int.append(1)
            else:
                row_int.append(float('inf'))
        grille_int.append(row_int)
    return grille_int

    
    
def trouver_chemin(grille,depart,arrivee):
    """
    Trouve un chemin entre deux points sur une grille en utilisant l'algorithme a_star.
    
    Entrées :
        grille : liste 2D
        depart : tuple indiquant les coordonées du point de départ
        arrivee: tuple indiquant les coordonées du point d'arrivé
    Sorties:
        chemin : Liste de coordonnées 2D représentant le chemin trouvé du point de départ au point d'arrivée trouvé par la fonction a star 
    """
    nouvelle_grille = str_vers_int(grille)
    return a_star(nouvelle_grille, depart, arrivee)
    
    
def chemin_bloque(grid_a_tester, start, goal):
    """
    Vérifie si le chemin entre deux points est bloqué dans une grille à tester. Utilise la fonction trouver_chemin
    
    Entrées :
        grille_a_tester : liste 2D 
        start : Coordonnées du point de départ sous forme (ligne, colonne).
        goal : Coordonnées du point d'arrivée sous forme (ligne, colonne).
    Sorties:
        bloque : booléen indiquant s'il existe un chemin entre start et goal avec la grille à tester
    """
    bloque = True
    path = trouver_chemin(grid_a_tester, start, goal)
    if path != []:
        bloque = False
    return bloque












