
import random

def create_map(rows,cols):
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            terrain = random.choice(['normal', 'forest', 'mountain','normal','normal','normal'])
            if terrain == 'normal':
                row.append(1)
            elif terrain == 'forest':
                row.append(3)
            elif terrain == 'mountain':
                row.append(float('inf'))  # Impassable
        grid.append(row)
    return grid

# Function to visualize the grid and the path
def visualize_grid(grid, path=None):
    visualization = []
    for i, row in enumerate(grid):
        visual_row = []
        for j, value in enumerate(row):
            if path and (i, j) in path:
                visual_row.append('P')  # Path
            elif value == 1:
                visual_row.append('.')  # Normal tile
            elif value == 3:
                visual_row.append('F')  # Forest
            elif value == float('inf') or value == 100:
                visual_row.append('M')  # Mountain (impassable)
        visualization.append(' '.join(visual_row))
    for line in visualization:
        print(line)