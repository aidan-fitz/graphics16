#!/usr/bin/python

from display import *
from draw import *
from draw3d import *
from parser import *
from matrix import *

import sys

screen = new_screen()
pen = [0, 255, 0]
polygons = []

fname = None
if len(sys.argv) >= 2:
    fname = sys.argv[1]
else:
    fname = '/dev/stdin'

parse_file( fname, screen, pen )
