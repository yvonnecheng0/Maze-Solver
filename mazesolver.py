""""
Module generates a maze and its solution path using a dfs algorithm given the width and height desired 
Yvonne Cheng 
csci 112
Winter, 2023
"""

import random
import matplotlib.pyplot as plt

def adjacent_pairs(width, height):
    #Initialize empty list
    adjacent_pairs = []

    #Add adjacent pairs for horizontal walls
    for y in range(height):
        for x in range(width - 1):
            curr_cell = y * width + x
            adjacent_pairs.append((curr_cell, curr_cell + 1))

    #Add adjacent pairs for vertical walls
    for y in range(height - 1):
        for x in range(width):
            curr_cell = y * width + x
            adjacent_pairs.append((curr_cell, curr_cell + width))

    #Remove walls for entrance and exit
    adjacent_pairs.remove((0, 1))  #Remove top left wall
    adjacent_pairs.remove((width * height - 1 - width, width * height - 1))  #Remove bottom right wall

    return adjacent_pairs

#Find root of a cell from parents
def root(cell, parents):
    #Update parent of current cell if parent of cell is not None 
    while parents[cell] is not None:
        cell = parents[cell]
    return cell

#Join two sets of cells in different sets to one set
def join(cell1, cell2, parents, sizes, removed_walls):
    #Initialize roots 
    root1 = root(cell1, parents)
    root2 = root(cell2, parents)

    #If root1 != root2, check which root has a smaller size
    if root1 != root2:
        #If root1 has smaller size than root2, roots are swapped
        if sizes[root1] < sizes[root2]:
            root1, root2 = root2, root1
        #Set parent of root2 = root1, joining the two set 
        parents[root2] = root1
        #Increase size of root1 by size of root2
        sizes[root1] += sizes[root2]
        #Add tuple of (cell1, cell2) to removed_walls
        removed_walls.append((cell1, cell2))

#Loop through list of walls and eliminate one by one 
def erase_walls(walls, parents, sizes):
    #Set random seed
    random.seed(1234)
    #Randomly shuffle list of walls
    random.shuffle(walls)
    remaining_walls = []
    removed_walls = []

    #Check if two cells on either side of wall are part of same root
    for wall in walls:
        cell1, cell2 = wall
        #If they aren't join two cells into the same root by removing wall between them, and add that wall to list of removed walls
        if root(cell1, parents) != root(cell2, parents):
            join(cell1, cell2, parents, sizes, removed_walls)
            continue
        
        #Add wall to list of remaining walls
        remaining_walls.append(wall)

    return remaining_walls, removed_walls

def generate_maze(width, height):

    #Create list of all possible adjacent pairs of cells in maze using adjacent_pairs 
    walls = adjacent_pairs(width, height)

    #Parents dictionary assigns a value of None to each cell in the maze
    parents = {cell: None for cell in range(width * height)}

    #Sizes dictionary assigns a value of 1 to each cell in the maze
    sizes = {cell: 1 for cell in range(width * height)}

    #Set remaining_walls, removed_walls = erase_walls
    remaining_walls, removed_walls = erase_walls(walls, parents, sizes)
    
    return remaining_walls, removed_walls

def position(cell, maze_size):
    #Set rows and cols of maze = maze_size
    nrows, ncols = maze_size

    #Calculate row index of cell 
    row = cell // ncols

    #Calculate col index of cell 
    col = cell % ncols

    return row, col

def adjacency_list(removed_walls, maze_size):
    #Initialize adj dictionary 
    predecessor = {}

    #Initialize adjacency list with empty lists for each cell
    for i in range(maze_size[0] * maze_size[1]):
        predecessor[i] = []

    #Loop through removed walls and add edges to adjacency list
    for wall in removed_walls:
        cell1, cell2 = wall
        predecessor[cell1].append(cell2)
        predecessor[cell2].append(cell1)

    return predecessor


def dfs(predecessor, maze_size):
    #Initialize variables
    start = 0  #Start at top left corner
    end = maze_size[0] * maze_size[1] - 1  #End at bottom right corner
    visited = set()
    path = []
    stack = [(start, [start])]

    #Loop if there are still cells to explore
    while stack:
        curr, curr_path = stack.pop()

        #If current cell is end cell, we have found the solution
        if curr == end:
            path = curr_path
            break

        #Add current cell to visited set
        visited.add(curr)

        #Reverse list of neighbors for current cell to explore cells in top-left to bottom-right order
        neighbors = predecessor[curr][::-1]

        #Loop through adjacent cells
        for neighbor in neighbors:
            #If neighbor has not been visited, add to stack with current path
            if neighbor not in visited:
                stack.append((neighbor, curr_path + [neighbor]))

    return path

def draw_maze(remaining_walls, removed_walls, maze_size, solution=[]):
    #Set rows and cols of maze = maze_size
    nrows, ncols = maze_size

    #Set up figure and axis object
    fig, ax = plt.subplots()

    #Turn off the axis
    ax.axis('off')

    #Draw four outer walls of maze
    plt.plot((0, ncols), (nrows, nrows), linestyle='-', color='black')
    plt.plot((ncols, ncols), (nrows, 0), linestyle='-', color='black')
    plt.plot((ncols, 0), (0, 0), linestyle='-', color='black')
    plt.plot((0, 0), (0, nrows), linestyle='-', color='black')

    #Don't draw top-left and bottom-right walls
    plt.plot((0, 1), (nrows, nrows), linestyle='-', color='white')
    plt.plot((ncols-1, ncols), (0, 0), linestyle='-', color='white')

    #Loop through remaining_walls list
    for wall in remaining_walls:
        # Set up pair of integers in list to wall
        i, j = wall
        #Calculate position of wall in maze
        y1, x1 = position(i, maze_size)
        y2, x2 = position(j, maze_size)

        #Flip row indices
        y1 = nrows - y1 - 1
        y2 = nrows - y2 - 1

        #Draw wall on plot
        if abs(x1 - x2) == 1:
            #Vertical wall
            plt.plot((max(x1, x2), max(x1, x2)), (y1, y1 + 1), linestyle='-', color='black')
        elif abs(y1 - y2) == 1:
            #Horizontal wall
            plt.plot((x1, x1 + 1), (max(y1, y2), max(y1, y2)), linestyle='-', color='black')

    #Draw solution
    if solution:
        #Reverse solution to start from the top-left corner
        solution = list(reversed(solution))
        #Loop through solution and draw line connecting each pair of adjacent cells along path
        for i in range(len(solution)-1):
            y1, x1 = position(solution[i], maze_size)
            y2, x2 = position(solution[i+1], maze_size)
            #Calculate coordinates of centers of two cells and draw a line connecting them
            center1 = (x1 + 0.5, nrows - y1 - 0.5)
            center2 = (x2 + 0.5, nrows - y2 - 0.5)
            plt.plot((center1[0], center2[0]), (center1[1], center2[1]), color='red', linewidth=2)

    #Display maze
    plt.show()


if __name__ == "__main__":
    maze_size = (50,50)
    remaining_walls, removed_walls = generate_maze(*maze_size)

    #Create adjacency list representation of the maze graph
    predecessor = adjacency_list(removed_walls, maze_size)

    #Solve maze using predecessor list
    solution = dfs(predecessor, maze_size)

    #Draw maze with solution highlighted
    draw_maze(remaining_walls, removed_walls, maze_size, solution)




