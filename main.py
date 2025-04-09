import heapq

# Direction vectors for moving up, down, left, right (no diagonal movement)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Function to calculate the Manhattan distance
def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# A* algorithm for pathfinding
def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    
    # Cost from start to the current node
    g_costs = [[float('inf')] * cols for _ in range(rows)]
    g_costs[start[0]][start[1]] = 0

    # Estimated cost from current node to goal
    f_costs = [[float('inf')] * cols for _ in range(rows)]
    f_costs[start[0]][start[1]] = manhattan_distance(start, goal)

    # Priority queue to explore nodes (min-heap)
    open_list = []
    heapq.heappush(open_list, (f_costs[start[0]][start[1]], start))

    # Track the path
    came_from = {}

    while open_list:
        # Get the node with the lowest f-cost
        current_f_cost, current = heapq.heappop(open_list)
        x, y = current

        # If we reach the goal, reconstruct the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()  # Reverse to get path from start to goal
            return path
        
        # Explore neighbors
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
    
    # If no path was found
    return None

# Example map: 50x70 grid with random terrain values (mountains have infinite cost)
def create_map():
    import random
    rows, cols = 20, 30
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

# Test the A* algorithm
if __name__ == "__main__":
    grid = create_map()
    #grid = [[1, 1, 1, 1, 1],[1, 100, 100, 100, 1],[1, 1, 1, 1, 1],[1, 100, 100, 100, 1],[1, 1, 1, 1, 1]]

    print("Initial Grid:")
    visualize_grid(grid)
    
    start = (0, 0)  # Starting point (top-left corner)
    goal = (19, 29)  # Goal point (bottom-right corner)

    # Find the path using A* algorithm
    path = a_star(grid, start, goal)

    # Visualize the grid with the path
    if path:
        print("Path found:")
        visualize_grid(grid, path)
    else:
        print("No path found.")
