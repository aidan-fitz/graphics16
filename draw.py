from display import *
from matrix import *
from math import *

def add_circle( points, cx, cy, cz, r, step ):
    # Find the first point
    x0 = cx + r
    y0 = cy
    for t in xrange(step, 1 + step, step):
        # Find the next point
        x1 = cx + r * cos(t * 2 * pi)
        y1 = cy + r * sin(t * 2 * pi)
        # Add the edge (x0, y0) => (x1, y1)
        add_edge(points, x0, y0, cz, x1, y1, cz)
        # Advance the point-er
        x0 = x1
        y0 = y1

HERMITE = 0
BEZIER = 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    # Find the first point
    xi = x0
    yi = y0
    # Setup transformation matrix
    T = None
    if curve_type == HERMITE:
        T = make_hermite()
    elif curve_type == BEZIER:
        T = make_bezier()
    # Generate curve coefficients
    coeffx = generate_curve_coeffs(x0, x1, x2, x3, T)
    coeffy = generate_curve_coeffs(y0, y1, y2, y3, T)
    # Iterate
    for t in xrange(step, 1 + step, step):
        # Find the next point
        xf = eval_poly(coeffx, t)
        yf = eval_poly(coeffy, t)
        # Add the edge (xi, yi) => (xf, yf)
        add_edge(points, xi, yi, 0, xf, yf, 0)
        # Advance the point-er
        xi = xf
        yi = yf

def draw_lines( matrix, screen, color ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1],
                   matrix[p+1][0], matrix[p+1][1], color )
        p += 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( screen, x0, y0, x1, y1, color ):
    dx = x1 - x0
    dy = y1 - y0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    
    if dx == 0:
        y = y0
        while y <= y1:
            plot(screen, color,  x0, y)
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            plot(screen, color, x, y0)
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx

