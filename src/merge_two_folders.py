import os
import shutil
import sys


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


if len(sys.argv) != 4:
        print("Usage: python merge_two_folders.py <path_folder1> <path_folder2> <merged_output_folder>")
else:
    folder1_path = sys.argv[1]
    folder2_path = sys.argv[2]
    merged_out_folder = sys.argv[3]
    # folder1_path = "/media/datassd/sina/perf-characterization/data/mixing_multiple_runs/50-start-5-indexed"
    # folder2_path = "/media/datassd/sina/perf-characterization/data/mixing_multiple_runs/150-start-5-indexed"
    # merged_out_folder = "/media/datassd/sina/perf-characterization/data/mixing_multiple_runs/merged_50_150"

    csv_files1 = [file for file in os.listdir(folder1_path) if file.endswith("_index.csv")]
    num_start_points1 = len(csv_files1)

    csv_files2 = [file for file in os.listdir(folder2_path) if file.endswith("_index.csv")]
    updated_files2 = update_file_ids(csv_files2, num_start_points1)

    os.makedirs(merged_out_folder, exist_ok=True)

    for file in csv_files1:
        shutil.copy2(os.path.join(folder1_path, file), os.path.join(merged_out_folder, file))
        non_index_file = file.replace("_index", "")
        shutil.copy2(os.path.join(folder1_path, non_index_file), os.path.join(merged_out_folder, non_index_file))

    for file, updated_file in zip(csv_files2, updated_files2):
        shutil.copy2(os.path.join(folder2_path, file), os.path.join(merged_out_folder, updated_file))
        non_index_file = file.replace("_index", "")
        non_index_updated_file = updated_file.replace("_index", "")
        shutil.copy2(os.path.join(folder2_path, non_index_file), os.path.join(merged_out_folder, non_index_updated_file))