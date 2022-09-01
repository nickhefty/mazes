import numpy as np
from random import sample
from render_maze import show_maps

#start and end row
START_ROW = -1
FINISH_ROW = 0

#constants defining ints in the matrix
VACANT = 0
PATH = 1
MINE = 2
CURRENT_POS = 3
 
#global constants that are updated by the recursive move function
COUNTER = 0
MAPS = []


def make_canvas(height, width=None):
    if width is None: width = height
    return np.matrix( [ [ VACANT ] * width ] * height)


def move(canvas, include_mirrors=False):
    #import global variables
    global COUNTER
    global MAPS
    
    #create a new copy of the canvas
    canvas = np.matrix.copy(canvas)
    
    #find the current position as coordinates
    location = np.where(canvas == CURRENT_POS)
    current_pos = location[0][0], location[1][0]
    
    #if we made it to the end row
    if current_pos[0] == FINISH_ROW: 
        canvas[current_pos] = PATH
        COUNTER += 2 if include_mirrors else 1
        #save the solution and it's mirror
        MAPS.append(canvas)
        if include_mirrors: MAPS.append(np.flip(canvas, 1))
        #return to make more solutions
        return
    
    #generate all four potential moves
    options = [
        (current_pos[0] + 1, current_pos[1]),
        (current_pos[0] - 1, current_pos[1]),
        (current_pos[0], current_pos[1] + 1),
        (current_pos[0], current_pos[1] - 1),
    ]

    #create a new list of the potential moves that are possible and follow the rules
    possible_moves = []
    for op in options:
        try:
            if canvas[op] == VACANT and all([i >= 0 for i in op]):
                possible_moves.append(op)
        except IndexError:
            pass
    
    #make next possible move
    for next_move in possible_moves:

        #block off each pssible move
        for mine in possible_moves:
            canvas[mine] = MINE

        #make the current position part of the path
        canvas[current_pos] = PATH

        #make the next move the current position
        canvas[next_move] = CURRENT_POS

        #recursively make the next move
        move(canvas, include_mirrors=include_mirrors)



def generate_maps(height):
        
    #generate all paths from each possible starting point
    for i in range( height // 2 ):  
        canvas = make_canvas(height)
        #block the entire bottom row
        canvas[START_ROW] = [MINE] * height
        #select the starting position
        canvas[START_ROW,i] = CURRENT_POS

        #begin recursively exploring the map
        move(canvas, include_mirrors=True)
        print(f'Maps generated from starting point ({START_ROW}, {i})\nTotal Maps: {COUNTER}')


generate_maps(8)
show_maps(sample(MAPS, 50), 8, 100, save=True)