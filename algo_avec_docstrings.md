import heapq
import main


# Direction des vecteurs de déplacement : haut, bas, gauche, droite
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


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
    fonction qui trouve le plus court chemin entre la position de départ et l'arrivée'
        Entrées:grid, grid
                start, coordonées du point de départ, liste
                goal, coordonées du point d'arrivé, liste
        Sortie: chemin le plus court, liste de coordonées, liste 2D
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


def chemin_bloque(grid_a_tester):
    """
    fonction qui cherche si il y a un passage possible sur une grid donnée
        Entrées:grid, grille à tester, grid
        Sortie: booléen
    """       
    bloque = True
    start = [0,0]
    goal = [main.rows-1,main.cols-1]
    path = a_star(grid_a_tester, start, goal)

    if path != []:
        bloque = False
    return bloque
