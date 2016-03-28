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
    print len(points)
    for x, y, z in sphere:
        print (x, y, z)
        add_edge(points, x, y, z, x, y, z)
    print len(points)

def generate_sphere(cx, cy, cz, r, step ):
    points = []
    # Add the top and bottom points only once
    points.append((r, 0, 0))
    points.append((-r, 0, 0))
    # then start with theta and phi
    d_theta = step * pi
    d_phi = d_theta * 2
    theta = d_theta
    # cache tau
    tau = 2 * pi
    while theta < pi:
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
    return points

def add_torus( points, cx, cy, cz, r, R, step ):
    torus = generate_torus(cx, cy, cz, r, R, step)
    for x, y, z in torus:
        print (x, y, z)
        add_edge(points, x, y, z, x, y, z)

def generate_torus(cx, cy, cz, r, R, step ):
    points = []
    # cache tau
    tau = 2 * pi
    # start with theta and phi
    dt = step * tau
    theta = 0
    while theta < tau:
        # cache cos and sin while the same theta is in use
        x = r * cos(theta)
        w = r * sin(theta) + R
        # Need to reset phi
        phi = 0
        while phi < tau:
            #print theta, phi
            y = w * cos(phi)
            z = w * sin(phi)
            points.append((x + cx, y + cy, z + cz))
            phi += dt
        theta += dt
    return points
