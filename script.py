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
    ident(t)
    systems = [ t ]
    screen = new_screen()
    tmp = []
    step = 0.1
    edges = []
    #push pop move/rotate/scale box/sphere/torus line save display
    for command in commands:
        print command
        if command[0]=='push':
            systems.append( [x[:] for x in systems[-1]] )
        elif command[0]=='pop':
            systems.pop()
        elif command[0] == 'box':
            add_box(edges, float(command[1]), float(command[2]), float(command[3]), float(command[4]), float(command[5]), float(command[6]))
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
        elif command[0] == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(edges,
                       float(command[1]), float(command[2]), float(command[3]),
                       float(command[4]), step)
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif command[0] == 'torus':
            #print 'TORUS\t' + str(command)
            add_torus(edges,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), step)
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
            
        elif command[0] == 'line':
                        #print 'LINE\t' + str(command)
            add_edge( edges,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), float(command[6]) )

        elif command[0] == 'rotate':
            print 'ROTATE\t' + str(command)
            theta = float(command[2]) * (math.pi / 180)
            
            if command[1] == 'x':
                t = make_rotX(theta)
            elif command[1] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif command[0] == 'scale':
            #print 'SCALE\t' + str(command)
            t = make_scale(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif command[0] == 'move':
            #print 'MOVE\t' + str(command)
            t = make_translate(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif command[0]=='display' or command[0]=='save':
            if command[0] == 'display':
                display(screen)
            else:
                save_extension(screen, command[1])
            
            
