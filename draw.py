from display import *
from matrix import *
from math import *

class BoxVertices:
    def __init__(self, x, y, z, width, height, depth):
        self.i = 0
        self.x0 = x
        self.y0 = y
        self.z0 = z
        self.x1 = x + width
        self.y1 = y + height
        self.z1 = z + depth

    def __iter__(self):
        return self

    def next(self):
        if self.i > 7:
            raise StopIteration
        else:
            L = []
            L.append(self.x0 if self.i & 1 else self.x1)
            L.append(self.y0 if self.i & 2 else self.y1)
            L.append(self.z0 if self.i & 4 else self.z1)
            self.i += 1
            return tuple(L)

def add_box( points, x, y, z, width, height, depth ):
    for px, py, pz in BoxVertices(x, y, z, width, height, depth):
        add_edge(points, px, py, pz, px, py, pz)

def add_sphere( points, cx, cy, cz, r, step ):
    sphere = generate_sphere(cx, cy, cz, r, step)
    for P in sphere:
        points.extend([P, P])

def generate_sphere(cx, cy, cz, r, step ):
    points = []
    # Add the top and bottom points only once
    points.append([r, 0, 0, 1])
    points.append([-r, 0, 0, 1])
    # then start with theta and phi
    d_theta = step * pi
    d_phi = d_theta * 2
    theta = d_theta
    phi = d_phi
    # cache tau
    tau = 2 * pi
    while theta < pi:
        # cache cos and sin while the same theta is in use
        x = r * cos(theta)
        w = r * sin(theta)
        while phi < tau:
            y = w * cos(phi)
            z = w * sin(phi)
            points.append([x + cx, y + cy, z + cz, 1])
            phi += d_phi
        theta += d_theta
    return points

def add_torus( points, cx, cy, cz, r, R, step ):
    torus = generate_torus(cx, cy, cz, r, R, step)
    for P in torus:
        points.extend([P, P])

def generate_torus(cx, cy, cz, r, R, step ):
    points = []
    # cache tau
    tau = 2 * pi
    # start with theta and phi
    dt = step * tau
    theta = 0
    phi = 0
    while theta < tau:
        # cache cos and sin while the same theta is in use
        x = r * cos(theta)
        w = r * sin(theta) + R
        while phi < tau:
            y = w * cos(phi)
            z = w * sin(phi)
            points.append([x + cx, y + cy, z + cz, 1])
            phi += dt
        theta += dt
    return points
    


def add_circle( points, cx, cy, cz, r, step ):
    # Find the first point
    x0 = cx + r
    y0 = cy
    t = 0

    tau = 2*pi
    while t < 1 + step:
        # Find the next point
        x1 = cx + r * cos(t * tau)
        y1 = cy + r * sin(t * tau)
        # Add the edge (x0, y0) => (x1, y1)
        add_edge(points, x0, y0, cz, x1, y1, cz)
        # Advance the point-er
        t += step
        x0 = x1
        y0 = y1

HERMITE = 0
BEZIER = 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    # Find the first point
    xi = x0
    yi = y0
    
    # Generate curve coefficients
    coeffx = generate_curve_coeffs(x0, x1, x2, x3, curve_type)
    coeffy = generate_curve_coeffs(y0, y1, y2, y3, curve_type)
    
    # Iterate
    t = 0
    while t < 1 + step:
        # Find the next point
        xf = eval_poly(coeffx, t)
        yf = eval_poly(coeffy, t)
        # Add the edge (xi, yi) => (xf, yf)
        add_edge(points, xi, yi, 0, xf, yf, 0)
        print 't: ', t, '\tx: ', xi, xf, '\ty: ', yi, yf
        # Advance the point-er
        t += step
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

