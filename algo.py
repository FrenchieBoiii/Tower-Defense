import heapq

# Direction vectors for moving up, down, left, right (no diagonal movement)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Function to calculate the Manhattan distance
def manhattan_distance(start, end):
    """
    fonction qui définie la distance Manhattan, distance entre 2 points avec des déplacment horizontaux et verticaux
        Entree: start, coordonnée point de départ, liste
        Sortie: distance Manhattan, int
    """    
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# A* algorithm for pathfinding
def a_star(grid, start, goal):
    """
    fonction qui trouve le chemin le plus court entre deux points sur une grille en utilisant l'algorithme A*'
        Entrées:grid, grid
                start, coordonées du point de départ
                goal, coordonées du point d'arrivé
        Sortie: chemin le plus court,  Liste des coordonnées représentant le chemin trouvé du point de départ au point d'arrivée, liste 2D
     
    """  
    rows, cols = len(grid), len(grid[0])
    
    # Cost from start to the current node
    g_costs = [[float('inf')] * cols for i in range(rows)]
    g_costs[start[0]][start[1]] = 0

    # Estimated cost from current node to goal
    f_costs = [[float('inf')] * cols for i in range(rows)]
    f_costs[start[0]][start[1]] = manhattan_distance(start, goal)

    # Priority queue to explore nodes (min-heap)
    open_list = []
    heapq.heappush(open_list, (f_costs[start[0]][start[1]], start))

    # Track the path
    came_from = {}
    path = []
    continuer = True
    
    while open_list and continuer:
        # Get the node with the lowest f-cost
        current_f_cost, current = heapq.heappop(open_list)
        x, y = current

        # If we reach the goal, reconstruct the path
        if current == goal:
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()  # Reverse to get path from start to goal
            continuer = False
        
        # Explore neighbors
        
        if continuer:
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
    
                # Ensure the neighbor is within the grid bounds
                if 0 <= nx < rows and 0 <= ny < cols:
                    # Mountain tiles are impassable
                    if grid[nx][ny] == float('inf'):
                        continue
    
                    # Calculate the cost to move to this neighbor
                    move_cost = grid[nx][ny]
                    tentative_g_cost = g_costs[x][y] + move_cost
    
                    # If this path is better, update costs and add to open list
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

    Entrée :
        grille : liste 2D
    
    Sortie : 
        grille : liste 2D
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
        depart : Coordonnées du point de départ sous forme (ligne, colonne).
        arrivee : Coordonnées du point d'arrivée sous forme (ligne, colonne).
    """
    nouvelle_grille = str_vers_int(grille)
    return a_star(nouvelle_grille, depart, arrivee)
    
    
def chemin_bloque(grid_a_tester, start, goal):
    """
    Vérifie si le chemin entre deux points est bloqué dans une grille. Utilise la fonction trouver_chemin
    
    Entrées :
        grille_a_tester : liste 2D
        start : Coordonnées du point de départ sous forme (ligne, colonne).
        goal : Coordonnées du point d'arrivée sous forme (ligne, colonne).

    """
    
    bloque = True
    
    path = trouver_chemin(grid_a_tester, start, goal)

    if path != []:
        bloque = False
    return bloque












