import mdl
from display import *
from matrix import *
from draw import *
from stack import Stack

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

    for command in commands:
        print command
