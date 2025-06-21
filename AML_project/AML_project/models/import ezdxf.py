import ezdxf
import os
import math

output_dir = "pentagons"
os.makedirs(output_dir, exist_ok=True)

def generate_pentagon(side_length):
    # Calculate radius of circumscribed circle
    angle = math.pi / 5
    radius = side_length / (2 * math.sin(angle))
    
    points = []
    for i in range(5):
        theta = 2 * math.pi * i / 5  # angle for each vertex
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((x, y))
    return points

# Generate 50 unique side lengths: 10 to 59 mm
for i, side_length in enumerate(range(10, 60), start=1):
    points = generate_pentagon(side_length)

    doc = ezdxf.new(dxfversion="R2010")
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()

    doc.header['$LIMMIN'] = (0, 0)
    doc.header['$LIMMAX'] = (1000, 1000)

    msp.add_lwpolyline(points, close=True)

    filename = f"pentagon_{i}.dxf"
    doc.saveas(os.path.join(output_dir, filename))

print("Generated 50 pentagon DXF files in the 'pentagons' folder.")