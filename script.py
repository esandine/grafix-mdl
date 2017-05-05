import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    t = new_matrix()
    systems = [ t ]
    screen = new_screen()
    tmp = []
    step = 0.1
    edges = []
    #push pop move/rotate/scale box/sphere/torus line save display
    for command in commands:
        if command[0]=='push':
            systems.append( [x[:] for x in systems[-1]] )
        elif command[0]=='pop':
            systems.pop()
        elif command[0] == 'box':
            add_box(edges, float(command[1]), float(command[2]), float(command[3]), float(command[4]), float(command[5]), float(command[6]))
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
        elif command[0]=='display' or command[0]=='save':
            if command[0] == 'display':
                display(screen)
            else:
                save_extension(screen, command[1])
            
            
