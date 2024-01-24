import os
import numpy as np

def count_instances_in_annotations(annotations_folder):
    class_counts = {}

    # Iterate through all annotation files in the folder
    for filename in os.listdir(annotations_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(annotations_folder, filename)

            # Read annotation file
            with open(filepath, 'r') as file:
                lines = file.readlines()

            # Extract class information from each line
            for line in lines:
                class_id = int(line.split()[0])

                # Increment the count for the class
                class_counts[class_id] = class_counts.get(class_id, 0) + 1

    return class_counts

def main():
    # Input: Path to the folder containing annotation files
    annotations_folder = "F:/TEETH_project/new sets to train/Batch2_ready_dataset/yolov8_1280-640_bal/labels - copy"

    # Get the class counts
    class_counts = count_instances_in_annotations(annotations_folder)

    # Output: Display the class counts
    for class_id, count in class_counts.items():
        print(f"Class {class_id}: {count} instances")

if __name__ == "__main__":
    main()
