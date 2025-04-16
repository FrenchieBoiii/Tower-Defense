from algo import a_star
from mapp import visualize_grid,create_map


rows, cols = 20, 30

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
