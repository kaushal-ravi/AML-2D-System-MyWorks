import ezdxf
import os
import math

def is_line_short(line, threshold=1e-3):
    start = line.dxf.start
    end = line.dxf.end
    distance = math.dist(start, end)
    return distance < threshold

def are_lines_identical(line1, line2, tolerance=1e-6):
    # Compare both directions (A→B and B→A)
    pts1 = (line1.dxf.start, line1.dxf.end)
    pts2 = (line2.dxf.start, line2.dxf.end)
    return (
        all(math.dist(p1, p2) < tolerance for p1, p2 in zip(pts1, pts2)) or
        all(math.dist(p1, p2) < tolerance for p1, p2 in zip(pts1[::-1], pts2))
    )

def optimize_dxf(input_path, output_path):
    doc = ezdxf.readfile(input_path)
    msp = doc.modelspace()

    # Remove short or duplicate lines
    lines = list(msp.query('LINE'))
    lines_to_remove = set()

    for i, line in enumerate(lines):
        if is_line_short(line):
            lines_to_remove.add(line)
        for j in range(i + 1, len(lines)):
            if are_lines_identical(line, lines[j]):
                lines_to_remove.add(lines[j])

    for line in lines_to_remove:
        msp.delete_entity(line)

    doc.saveas(output_path)
    print(f"Optimized: {os.path.basename(input_path)} → {os.path.basename(output_path)}")

def process_all_dxf_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.dxf'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            optimize_dxf(input_path, output_path)

# === Usage ===
input_folder = r"AML-2D-System-MyWorks/AML_project/rhombuses"
output_folder = "rhombuses_optimized"
process_all_dxf_files(input_folder, output_folder)
