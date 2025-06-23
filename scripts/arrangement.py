import ezdxf
import os
import random
import math
from shapely.geometry import Polygon, Point
from shapely.affinity import translate, scale
from shapely import speedups

if speedups.available:
    speedups.enable()

# Constants
RECT_WIDTH = 200
RECT_HEIGHT = 150
MARGIN = 4  # mm spacing between shapes and from edges
NUM_FILES = 50
SHAPE_TYPES = ['circle', 'square', 'rectangle', 'triangle', 'pentagon', 'ellipse']
OUTPUT_FOLDER = r"C:\AML-kaushal\results"

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Geometry creation helpers
def create_circle(x, y, r):
    return Point(x, y).buffer(r), ('CIRCLE', (x, y, r))

def create_square(x, y, side):
    points = [(x, y), (x+side, y), (x+side, y+side), (x, y+side)]
    return Polygon(points), ('LWPOLYLINE', points)

def create_rectangle(x, y, w, h):
    points = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
    return Polygon(points), ('LWPOLYLINE', points)

def create_triangle(x, y, base):
    height = (math.sqrt(3)/2) * base
    points = [(x, y), (x + base/2, y + height), (x + base, y)]
    return Polygon(points), ('LWPOLYLINE', points)

def create_pentagon(x, y, radius):
    angle = 2 * math.pi / 5
    points = [(x + radius * math.cos(i * angle), y + radius * math.sin(i * angle)) for i in range(5)]
    poly = Polygon(points)
    minx, miny = poly.bounds[0], poly.bounds[1]
    poly = translate(poly, -minx + x, -miny + y)  # shift to position
    return poly, ('LWPOLYLINE', list(poly.exterior.coords)[:-1])

def create_ellipse(x, y, rx, ry):
    ellipse_shape = scale(Point(x, y).buffer(1), rx, ry)
    return ellipse_shape, ('ELLIPSE', (x, y, rx, ry))

# Shape generator
def generate_shape(shape_type, x, y):
    if shape_type == 'circle':
        r = random.uniform(5, 15)
        return create_circle(x, y, r)
    elif shape_type == 'square':
        s = random.uniform(10, 30)
        return create_square(x, y, s)
    elif shape_type == 'rectangle':
        w = random.uniform(15, 40)
        h = random.uniform(10, 25)
        return create_rectangle(x, y, w, h)
    elif shape_type == 'triangle':
        b = random.uniform(15, 35)
        return create_triangle(x, y, b)
    elif shape_type == 'pentagon':
        r = random.uniform(10, 20)
        return create_pentagon(x, y, r)
    elif shape_type == 'ellipse':
        rx = random.uniform(10, 20)
        ry = random.uniform(5, 15)
        return create_ellipse(x, y, rx, ry)

# Attempt to place shape in non-overlapping space
def place_shapes():
    placed_shapes = []
    geometry_list = []

    tries = 0
    max_tries = 1000

    num_shapes = random.randint(4, 8)

    while len(placed_shapes) < num_shapes and tries < max_tries:
        shape_type = random.choice(SHAPE_TYPES)
        x = random.uniform(MARGIN, RECT_WIDTH - MARGIN)
        y = random.uniform(MARGIN, RECT_HEIGHT - MARGIN)

        shape, draw_info = generate_shape(shape_type, x, y)
        shape = shape.buffer(MARGIN)  # add margin for spacing

        if shape.bounds[2] > RECT_WIDTH or shape.bounds[3] > RECT_HEIGHT:
            tries += 1
            continue

        # Check for overlap
        if all(not shape.intersects(existing) for existing in geometry_list):
            geometry_list.append(shape)
            placed_shapes.append(draw_info)
        tries += 1

    return placed_shapes

# Drawing creator
def create_dxf(filename, shapes):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Draw boundary
    msp.add_lwpolyline([
        (0, 0), (RECT_WIDTH, 0), (RECT_WIDTH, RECT_HEIGHT),
        (0, RECT_HEIGHT), (0, 0)
    ], close=True)

    for shape in shapes:
        if shape[0] == 'CIRCLE':
            x, y, r = shape[1]
            msp.add_circle((x, y), r)
        elif shape[0] == 'LWPOLYLINE':
            msp.add_lwpolyline(shape[1], close=True)
        elif shape[0] == 'ELLIPSE':
            x, y, rx, ry = shape[1]
            msp.add_ellipse(center=(x, y), major_axis=(rx, 0), ratio=ry/rx)

    doc.saveas(os.path.join(OUTPUT_FOLDER, filename))

# Main loop
for i in range(1, NUM_FILES + 1):
    shapes = place_shapes()
    fname = f"dataset_{i:02}.dxf"
    create_dxf(fname, shapes)
    print(f"[✓] Created: {fname}")
