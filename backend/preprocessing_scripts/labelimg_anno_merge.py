import os

def merge_files(directory1, directory2, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get the list of files in each directory
    files1 = os.listdir(directory1)
    files2 = os.listdir(directory2)

    # Find common filenames in both directories
    common_files = set(files1).intersection(files2)

    # Iterate through common filenames and merge corresponding files
    for filename in common_files:
        file1_path = os.path.join(directory1, filename)
        file2_path = os.path.join(directory2, filename)

        # Read content from both files
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            content1 = file1.read()
            content2 = file2.read()

        # Merge content
        merged_content = content1.strip() + '\n' + content2.strip()

        # Write merged content to the output directory
        output_path = os.path.join(output_directory, filename)
        with open(output_path, 'w') as output_file:
            output_file.write(merged_content)

        print(f"Merged: {filename}")

# Replace 'directory1' and 'directory2' with the actual paths to your directories
directory1 = 'F:/TEETH_project/new sets to train/batch1 and batch2 merge/Batch1_txt_labels'
directory2 = 'F:/TEETH_project/new sets to train/batch1 and batch2 merge/Batch2_txt_labels/Restoration'
output_directory = 'F:/TEETH_project/new sets to train/batch1 and batch2 merge/merged labels'

merge_files(directory1, directory2, output_directory)