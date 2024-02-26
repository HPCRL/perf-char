import os
import shutil
import pandas as pd
import sys

def get_unique_tile_size_files(folder_path):
    # Get a list of all CSV files with names ending in "_index.csv" in the folder
    csv_files = [file.replace("_index.csv", ".csv") for file in os.listdir(folder_path) if file.endswith("_index.csv")]

    # Set to store unique tile_size values
    unique_tile_sizes = set()

    # Set to store files with unique tile_size values
    unique_tile_size_files = set()

    # Loop through each CSV file
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)

        # Read the first row of the CSV file
        first_row = pd.read_csv(file_path, nrows=1)

        # Check if "tile_size" column exists in the first row
        # Get the unique value in the "tile_size" column
        tile_size_value = first_row['tile_sizes'].iloc[0]

        # Check if the tile_size value is already in the set
        if tile_size_value not in unique_tile_sizes:
            # Add the tile_size value to the set
            unique_tile_sizes.add(tile_size_value)
            # Add the file to the set of unique_tile_size_files
            unique_tile_size_files.add(csv_file)
        else:
            print("Repeatative Start Point")

    return unique_tile_size_files

'''
def update_file_ids(file_list, start_id):
    updated_files = []
    for idx, file in enumerate(file_list):
        # base_name, extension = os.path.splitext(file)
        parts = file.split('cuda_')
        assert len(parts) == 2, f"File name has an issue: {file}"
        file_id = int(parts[0])
        assert isinstance(file_id, int), f"Conversion failed for {file}"
        updated_file = f"{start_id + file_id}_cuda{parts[1]}"
        # updated_file = f"{start_id + file_id}_{base_name}_index{extension}"
        updated_files.append(updated_file)
    return updated_files
'''

if len(sys.argv) != 3:
        print("Usage: python remove_dup_starts.py <input_folder> <output_folder>")
else:
    folder_path = sys.argv[1]
    dup_removed_folder = sys.argv[2]

    # Replace with the actual paths to your folders
    # folder_path = '/media/datassd/sina/perf-characterization/data/mixing_multiple_runs/merged_50_150'
    # dup_removed_folder = '/media/datassd/sina/perf-characterization/data/mixing_multiple_runs/merged_50_150_uniqued'

    # Get unique files from both folders
    unique_files = get_unique_tile_size_files(folder_path)
    print(len(unique_files))

    # Create the output folder if it doesn't exist
    os.makedirs(dup_removed_folder, exist_ok=True)

    # Copy unique files from the first folder to the output folder
    for file in unique_files:
        shutil.copy2(os.path.join(folder_path, file), os.path.join(dup_removed_folder, file))
        index_file = file.replace(".csv", "_index.csv")
        shutil.copy2(os.path.join(folder_path, index_file), os.path.join(dup_removed_folder, index_file))

