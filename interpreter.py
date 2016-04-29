import mdl
from display import *
from matrix import *
from matrix import matrix_mult as mmult
from draw import *
from draw3d import *
from stack import Stack

from math import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    # Setup drawing environment *after* the error checking to prevent prematurely allocating too much memory
    color = [255, 255, 255]
    stack = Stack()
    screen = new_screen()

    env = (color, stack, screen, symbols)

    # Pick a function to execute from the dict(string, function)
    x_map = {
        # 2-D drawing routines
        "line": line,
        "circle": circle,
        "hermite": hermite,
        "bezier": bezier,
        # 3-D drawing routines
        "box": box,
        "sphere": sphere,
        "torus": torus,
        # Matrix stack operations
        "push": push,
        "pop": pop,
        # Transformations
        "move": move,
        "scale": scale,
        "rotate": rotate,
        # Display and save
        "display": display_img,
        "save": save_img
    }

    for command in commands:
        print command
        cmd = command[0]
        x_map[cmd](command, env)

# Functions for executing commands

# 2-D drawing routines

def line(args, env):
    # Semantic analyzer
    x0, y0, z0, x1, y1, z1 = args[1:]
    color, stack, screen, symbols = env

    # Immediately draw line to screen
    edges = []
    add_edge(edges, x0, y0, z0, x1, y1, z1)
    mmult(stack.peek(), edges)
    draw_lines(edges, screen, color)

def circle(args, env):
    # Semantic analyzer
    pass

def hermite(args, env):
    pass

def bezier(args, env):
    pass

# 3-D drawing routines

def box(args, env):
    x, y, z, width, height, depth = args[1:]
    color, stack, screen, symbols = env

    polygons = []
    add_box(polygons, x, y, z, width, height, depth)
    mmult(stack.peek(), polygons)
    draw_polygons(polygons, screen, color)

def sphere(args, env):
    x, y, z, r, coord_system = args[1:]
    color, stack, screen, symbols = env

    step = int(round(2 * sqrt(r)))

    polygons = []
    add_sphere(polygons, x, y, z, r, step)
    mmult(stack.peek() if coord_system is None else coord_system, polygons)
    draw_polygons(polygons, screen, color)

def torus(args, env):
    pass
    #x, y, z, r, R, coord_system = args[1:]

# Matrix stack operations

def push(args, env):
    color, stack, screen, symbols = env

    stack.push()

def pop(args, env):
    color, stack, screen, symbols = env

    stack.pop()

# Transformations

def move(args, env):
    x, y, z, knob = args[1:]
    color, stack, screen, symbols = env

    u = make_translate(x, y, z)
    stack.mult(u)

def scale(args, env):
    x, y, z, knob = args[1:]
    color, stack, screen, symbols = env

    u = make_scale(x, y, z)
    stack.mult(u)

def rotate(args, env):
    axis, degrees, knob = args[1:]
    color, stack, screen, symbols = env

    rot = {
        "x": make_rotX,
        "y": make_rotY,
        "z": make_rotZ
    }

    u = rot[axis](radians(degrees))
    stack.mult(u)

# Display and save

def display_img(args, env):
    screen = env[2]
    display(screen)

def save_img(args, env):
    color, stack, screen, symbols = env
