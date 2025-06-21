import ezdxf
from ezdxf.units import MM
import random

# Create a new DXF document in mm
doc = ezdxf.new(dxfversion="R2010")
doc.units = MM
msp = doc.modelspace()

# Rectangle boundary size
box_width = 150
box_height = 100
padding = 5

# Draw boundary rectangle
msp.add_lwpolyline([
    (0, 0),
    (box_width, 0),
    (box_width, box_height),
    (0, box_height),
    (0, 0)
], dxfattribs={"closed": True})

# Generate 6 random shapes (mix of circles and rectangles)
for i in range(6):
    shape_type = random.choice(["circle", "rectangle"])
    if shape_type == "circle":
        radius = random.uniform(5, 10)
        x = random.uniform(padding + radius, box_width - radius - padding)
        y = random.uniform(padding + radius, box_height - radius - padding)
        msp.add_circle(center=(x, y), radius=radius)
    else:
        w = random.uniform(10, 20)
        h = random.uniform(10, 20)
        x = random.uniform(padding, box_width - w - padding)
        y = random.uniform(padding, box_height - h - padding)
        msp.add_lwpolyline([
            (x, y),
            (x + w, y),
            (x + w, y + h),
            (x, y + h),
            (x, y)
        ], dxfattribs={"closed": True})

# Save file
doc.saveas("sample_shapes_in_box.dxf")
print("Saved as sample_shapes_in_box.dxf")