import ezdxf
import os

# Output folder
output_dir = "circles"
os.makedirs(output_dir, exist_ok=True)

# Generate 60 unique radii from 10 to 69 mm
for i, radius in enumerate(range(10, 70), start=1):
    doc = ezdxf.new(dxfversion="R2010")
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()

    # Drawing limits (optional)
    doc.header['$LIMMIN'] = (0, 0)
    doc.header['$LIMMAX'] = (1000, 1000)

    # Add circle
    msp.add_circle(center=(0, 0), radius=radius)

    # Save file
    filename = f"circle_{i}.dxf"
    doc.saveas(os.path.join(output_dir, filename))

print("✅ Generated 60 circle DXF files in the 'circles' folder.")