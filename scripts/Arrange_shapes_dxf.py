import os
import ezdxf
import joblib
import numpy as np
from ezdxf.math import Vec2
from shapely.geometry import Polygon, Point
from sklearn.preprocessing import MinMaxScaler

# Load models
model = joblib.load(r'C:\AML-kaushal\AML-2D-System-MyWorks\AML_project\random_forest_model (1).pkl')
label_encoder = joblib.load(r'C:\AML-kaushal\AML-2D-System-MyWorks\label_encoder (1).pkl')
scaler = joblib.load(r'C:\AML-kaushal\AML-2D-System-MyWorks\minmax_scaler.pkl')

INPUT_DIR = r'C:\AML-kaushal\lol'
OUTPUT_DIR = r'C:\AML-kaushal\results'
SPACING = 4.0  # 4mm spacing


def extract_features(entity):
    if isinstance(entity, ezdxf.entities.LWPolyline) and entity.is_closed:
        points = [Vec2(p[:2]) for p in entity.get_points()]
        polygon = Polygon(points)
        area = polygon.area
        perimeter = polygon.length
        minx, miny, maxx, maxy = polygon.bounds
        width = maxx - minx
        height = maxy - miny
        aspect_ratio = width / height if height != 0 else 0
        return [area, perimeter, aspect_ratio, width, height]
    elif isinstance(entity, ezdxf.entities.Circle):
        radius = entity.dxf.radius
        area = np.pi * radius ** 2
        perimeter = 2 * np.pi * radius
        return [area, perimeter, 1.0, radius * 2, radius * 2]  # aspect_ratio = 1.0
    return None


def classify_shape(features):
    features_scaled = scaler.transform([features])
    label = model.predict(features_scaled)
    return label_encoder.inverse_transform(label)[0]


def arrange_shapes(shapes):
    arranged = []
    x_cursor = SPACING
    y_cursor = SPACING
    max_row_height = 0
    max_width = 500  # Max width of container rectangle

    for shape in shapes:
        width = shape['width']
        height = shape['height']

        if x_cursor + width + SPACING > max_width:
            x_cursor = SPACING
            y_cursor += max_row_height + SPACING
            max_row_height = 0

        shape['insert_point'] = (x_cursor, y_cursor)
        arranged.append(shape)

        x_cursor += width + SPACING
        max_row_height = max(max_row_height, height)

    return arranged


def transform_entity(entity, insert_point):
    if isinstance(entity, ezdxf.entities.LWPolyline):
        dx = insert_point[0] - min([p[0] for p in entity.get_points()])
        dy = insert_point[1] - min([p[1] for p in entity.get_points()])
        entity.translate(dx, dy)
    elif isinstance(entity, ezdxf.entities.Circle):
        dx = insert_point[0] - (entity.dxf.center.x - entity.dxf.radius)
        dy = insert_point[1] - (entity.dxf.center.y - entity.dxf.radius)
        entity.dxf.center = (entity.dxf.center.x + dx, entity.dxf.center.y + dy)


def process_file(file_path):
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    shapes = []

    for entity in msp:
        features = extract_features(entity)
        if features:
            label = classify_shape(features)
            minx, miny, maxx, maxy = Polygon([p[:2] for p in entity.get_points()]).bounds if hasattr(entity, 'get_points') else entity.bbox()
            shapes.append({
                'entity': entity,
                'label': label,
                'features': features,
                'width': maxx - minx,
                'height': maxy - miny
            })

    arranged = arrange_shapes(shapes)

    new_doc = ezdxf.new()
    new_msp = new_doc.modelspace()

    for shape in arranged:
        entity = shape['entity'].copy()
        transform_entity(entity, shape['insert_point'])
        new_msp.add_entity(entity)

    output_filename = os.path.basename(file_path)
    new_doc.saveas(os.path.join(OUTPUT_DIR, output_filename))


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith('.dxf'):
            print(f"Processing {filename}...")
            process_file(os.path.join(INPUT_DIR, filename))
    print("✅ All files processed and arranged.")