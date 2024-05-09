#!/usr/bin/env python3
# Write chmod +x mazegen.py for command line excecution

import sys
import random

MAX_DIM = 100
MIN_DIM = 5

def generateMaze(maze):
    sys.setrecursionlimit(1500);  # default limit doesn't allow for maze generation up to 100x100
    startX, startY = 0, 0
    nodesVisited = [(startX, startY)]
    carve(maze, startX, startY, nodesVisited, None, 1)
    nodesVisited.remove((0, 0))  # ensure that the end point can't equal the start point
    (endX, endY) = (random.choices(nodesVisited, weights = [(each[0]+each[1])**5 for each in nodesVisited], k = 1))[0]
    maze[startY][startX] = 'S'
    maze[endY][endX] = 'E'
    return maze

# Overview of function: the possible directions for the maze to go in are randomised,
# and iterated through until one of them is a a point in the list that hasn't been visited yet.
# A path will then be carved out in that direction, and the function is called recursively.
# This continues until every cell that could have a path has been visited, and all paths have
# been carved, at which point the function unwraps itself, leaving the completed maze.

# Extra features: Windiness: determines the likelyhood of the algorithm continuing to carve in the
# same direction. Higher values result in long, winding paths, smaller values result
# in a more grid-like structure.
# LoopChance: determines the likelyhood of carving into a space thats already been visited. Higher
# values result in more paths and loops in the maze
# StopChance: determines the likelyhood of not carving into a valid space. Higher values result in
# more dead ends in the maze.
def carve(maze, currentX, currentY, nodesVisited, lastDirection, windiness):
    directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
    counter = 0
    loopChance = 0.02
    stopChance = 0.06
    if lastDirection != None:
        while counter < windiness:
            directions.append(lastDirection)
            counter += 1;
    random.shuffle(directions)
    for each in directions:
        nx = currentX + each[0]
        ny = currentY + each[1]
        if (0 <= ny < len(maze)) and (0 <= nx < len(maze[0]) and random.random() > stopChance):
            if random.random() <= loopChance or ((nx, ny) not in nodesVisited):
                nodesVisited.append((nx, ny))
                maze[currentY + each[1] // 2][currentX + each[0] // 2] = ' '
                maze[ny][nx] = ' '
                carve(maze, nx, ny, nodesVisited, (each[0], each[1]), windiness)
        

    

def writeToFile (maze, filename):
    with open(filename, 'w') as file:
        file.write('\n'.join(''.join(i) for i in maze))


def main():
    #checking command line arguments
    if len(sys.argv) != 4:
        print("Invalid format. Format should be: ./mazeGen filename width height")
        exit(1)
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    if width > MAX_DIM or width < MIN_DIM or height > MAX_DIM or height < MIN_DIM:
        print("Invalid dimensions. Both width and height must be between 5 and 100")
        #exit(2)
    #creating the base for the maze
    grid = [["#" for i in range (width)] for j in range (height)]
    #generating maze and writing to file
    maze = generateMaze(grid)
    writeToFile(maze, sys.argv[1])


if __name__ == "__main__":
    main()