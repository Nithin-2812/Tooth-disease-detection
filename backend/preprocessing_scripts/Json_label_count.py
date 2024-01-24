

''' This program is to count the number of individual labels. Here we must provide the directory path of the json files'''

import json
import os

# Directory containing all annotation files
annotation_directory = 'F:/TEETH_project/new sets to train/Restorative jason' 

# Initialize class counts dictionary
total_class_counts = {}

# Loop through each annotation file in the directory
for filename in os.listdir(annotation_directory):
    if filename.endswith('.json'):
        # Load the annotation file
        file_path = os.path.join(annotation_directory, filename)
        with open(file_path, 'r') as file:
            annotation_data = json.load(file)

        # Extract class labels and count occurrences
        class_counts = {}
        for shape in annotation_data['shapes']:
            label = shape['label']
            if label in class_counts:
                class_counts[label] += 1
            else:
                class_counts[label] = 1

        # Accumulate counts to the total_class_counts dictionary
        for label, count in class_counts.items():
            if label in total_class_counts:
                total_class_counts[label] += count
            else:
                total_class_counts[label] = count

# Display the number of class labels and individual class label counts
num_classes = len(total_class_counts)
print(f"Number of class labels: {num_classes}")

print("\nIndividual class label counts:")
for label, count in total_class_counts.items():
    print(f"{label}: {count}")
