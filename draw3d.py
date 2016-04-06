from draw import *

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
            L.append(self.x1 if self.i & 1 else self.x0)
            L.append(self.y1 if self.i & 2 else self.y0)
            L.append(self.z1 if self.i & 4 else self.z0)
            self.i += 1
            return tuple(L)

def add_box( points, x, y, z, width, height, depth ):
    vertices = list(BoxVertices(x, y, z, width, height, depth))

    # indices of faces
    back = [2, 3, 1, 0]
    front = [i + 4 for i in back[::-1]]
    bottom = [0, 1, 5, 4]
    top = [(i + 6) % 8 for i in bottom]
    left = [0, 4, 6, 2]
    right = [i + 1 for i in left[::-1]]

    faces = [front, back, left, right, top, bottom]

    for face in faces:
        x0, y0, z0 = vertices[face[0]]
        x1, y1, z1 = vertices[face[1]]
        x2, y2, z2 = vertices[face[2]]
        x3, y3, z3 = vertices[face[3]]
        add_quad(points, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3)

# 'step' == number of steps (# points per ring)

# Generates 'step' rows and 'step' columns of shapes
# * 1 top row of triangles
# * 'step - 2' middle rows of quadrilaterals
# * 1 bottom row of triangles
def add_sphere( points, cx, cy, cz, r, step ):
    columns = generate_sphere(cx, cy, cz, r, step)

    for row, col in [(r, c) for r in range(step) for c in range(step)]:
        row1p = row + 1
        col1p = (col + 1) % step

        # Top row of triangles
        if row == 0:
            x0, y0, z0 = columns[col][row]
            x1, y1, z1 = columns[col][row1p]
            x2, y2, z2 = columns[col1p][row1p]
            add_triangle(points, x0, y0, z0, x1, y1, z1, x2, y2, z2)

        # Middle row
        elif row < step - 1:
            x0, y0, z0 = columns[col][row]
            x1, y1, z1 = columns[col][row1p]
            x2, y2, z2 = columns[col1p][row1p]
            x3, y3, z3 = columns[col1p][row]
            add_quad(points, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3)
        
        # Bottom row
        else:
            x0, y0, z0 = columns[col][row]
            x1, y1, z1 = columns[col][row1p]
            x2, y2, z2 = columns[col1p][row]
            add_triangle(points, x0, y0, z0, x1, y1, z1, x2, y2, z2)

'''
    for x, y, z in sphere:
        add_triangle(points, x, y, z, x, y, z, x, y, z)
'''

# Generates 'step + 1' rows and 'step' columns of points (an array of 'step' columns)
# Each column is a semicircle
# Each row is a circle
def generate_sphere(cx, cy, cz, r, step ):
    points = []
    # cache tau
    tau = 2 * pi
    # then start with theta and phi
    d_phi = tau / step
    d_theta = pi / step
    phi = 0

    while phi < tau:
        # templates for x, y
        tx = r * cos(phi)
        ty = r * sin(phi)
        # Need to reset theta
        theta = 0

        col = []
        while theta <= pi:
            w = sin(theta)
            x = tx * w
            y = ty * w
            z = r * cos(theta)
            col.append((x + cx, y + cy, z + cz))
            theta += d_theta
        points.append(col)

        phi += d_phi
    return points

''' while theta <= pi:
        # cache cos and sin while the same theta is in use
        x = r * cos(theta)
        w = r * sin(theta)
        # Need to reset phi
        phi = 0
        while phi < tau:
            #print theta, phi
            y = w * cos(phi)
            z = w * sin(phi)
            points.append((x + cx, y + cy, z + cz))
            phi += d_phi
        theta += d_theta
    return points'''

# Generates 'step' rows and 'step' columns of quadrilaterals
def add_torus( points, cx, cy, cz, r, R, step ):
    rows = generate_torus(cx, cy, cz, r, R, step)

    for row, col in [(r, c) for r in range(step) for c in range(step)]:
        row1p = (row + 1) % step
        col1p = (col + 1) % step

        # Pray to None that this is counterclockwise
        x0, y0, z0 = rows[row][col]
        x1, y1, z1 = rows[row1p][col]
        x2, y2, z2 = rows[row1p][col1p]
        x3, y3, z3 = rows[row][col1p]
        add_quad(points, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3)

'''
    for x, y, z in torus:
        add_triangle(points, x, y, z, x, y, z, x, y, z)
'''

# Generates 'step' rows and 'step' columns of points (an array of 'step' rows)
# Each column is a "small" circle
# Each row is a "big" circle in the yz plane
def generate_torus(cx, cy, cz, r, R, step ):
    points = []
    # cache tau
    tau = 2 * pi
    # start with theta and phi
    dt = tau / step
    theta = 0

    while theta < tau:
        # cache cos and sin while the same theta is in use
        x = r * cos(theta)
        w = r * sin(theta) + R
        # Need to reset phi
        phi = 0

        row = []
        while phi < tau:
            #print theta, phi
            y = w * cos(phi)
            z = w * sin(phi)
            row.append((x + cx, y + cy, z + cz))
            phi += dt
        points.append(row)

        theta += dt
    return points

# Routines for polygon matrices

def add_triangle( matrix, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    add_point(matrix, x2, y2, z2)

def add_quad( matrix, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3 ):
    add_triangle(matrix, x0, y0, z0, x1, y1, z1, x2, y2, z2)
    add_triangle(matrix, x2, y2, z2, x3, y3, z3, x0, y0, z0)

def draw_polygons(matrix, screen, color):
    if len(matrix) == 0:
        return

    if len(matrix) % 3:
        raise ValueError("Need 3 points to draw a triangle")

    for p in range(0, len(matrix), 3):
        draw_triangle(matrix, p, screen, color)

def draw_triangle(matrix, index, screen, color):
    # Shorthand for the three vertices
    p0 = matrix[index]
    p1 = matrix[index + 1]
    p2 = matrix[index + 2]

    # Scalar triple product of two edges a, b and the view vector k (kab) == k . a x b
    # We only need the x and y components since they will be included in the z component of a x b

    ax = p1[0] - p0[0]
    ay = p1[1] - p0[1]

    bx = p2[0] - p0[0]
    by = p2[1] - p0[1]

    nz = ax * by - bx * ay

    # if True:
    if nz >= 0:
        edges = [p0, p1, p1, p2, p2, p0]
        draw_lines(edges, screen, color)

