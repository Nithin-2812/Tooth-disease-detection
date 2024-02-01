

''' Input : folder in which both the json annotation files and there corresponding images are present
    output : converted yolo annotation files which resides in yolo_output_folder'''

import os
import json
from PIL import Image

def labelme_to_yolo(json_path, yolo_path, classes_file_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    image_path = os.path.join(os.path.dirname(json_path), data['imagePath'][27:])
    image = Image.open(image_path)
    img_width, img_height = image.size

    with open(classes_file_path, 'a') as classes_file:
        for shape in data['shapes']:
            class_name = shape['label']
            if class_name not in classes:
                classes.append(class_name)
                classes_file.write(f"{class_name}\n")

            class_idx = classes.index(class_name)
            points = shape['points']
            
            # Convert polygon to bounding box
            x_values = [point[0] for point in points]
            y_values = [point[1] for point in points]
            xmin = min(x_values) / img_width
            xmax = max(x_values) / img_width
            ymin = min(y_values) / img_height
            ymax = max(y_values) / img_height

            # Write to YOLO format
            yolo_line = f"{class_idx} {((xmin + xmax) / 2):.6f} {((ymin + ymax) / 2):.6f} " \
                        f"{(xmax - xmin):.6f} {(ymax - ymin):.6f}\n"
            with open(yolo_path, 'a') as yolo_file:
                yolo_file.write(yolo_line)

if __name__ == "__main__":
    # Set the paths
    labelme_json_folder = "F:/TEETH_project/new sets to train/labelme/Implants json" 
    yolo_output_folder = "F:/TEETH_project/new sets to train/labelimg/Implants" 
    classes_file_path = "F:/TEETH_project/labelmeTolabelimg/output/classes.txt"

    # Create a list to store class names
    classes = []

    # Process each LabelMe JSON file
    for json_file in os.listdir(labelme_json_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(labelme_json_folder, json_file)
            yolo_path = os.path.join(yolo_output_folder, json_file.replace('.json', '.txt'))
            labelme_to_yolo(json_path, yolo_path, classes_file_path)

    print("Conversion completed.")
