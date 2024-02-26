import pandas as pd
import sys
import os


def attach_column(mark_file_path, index_file_path):
    df_wmark = pd.read_csv(mark_file_path)
    mark_column = df_wmark['mark']
    tile_sizes_column = df_wmark['tile_sizes']
    index_df = pd.read_csv(index_file_path, header=None)
    index_df.insert(7, 7, mark_column)
    index_df.insert(8, 8, tile_sizes_column)
    output_file_path = index_file_path.replace('.csv', '_wmts.csv')
    index_df.to_csv(output_file_path, index=False, header=False)



if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python attach_mark_to_indexbased.py <path_to_index_based_csvs_folder>")
    else:
        directory_path = sys.argv[1]
        # file2_path = sys.argv[2]
        # attach_column(file1_path, file2_path)
    
        # directory_path = '/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output/mm5'
        # directory_path = '/media/datassd/sina/perf-characterization/chendi-repo/Characterization_data/_output'
        # directory_path = '/media/datassd/sina/perf-characterization/data/pz5-merged200'
        files = [f for f in os.listdir(directory_path) if f.lower().endswith('_index.csv') and os.path.isfile(os.path.join(directory_path, f))]

        # Iterate over each file
        file_counter = 1
        num_files = len(files)
        for file_name in files:
            index_file_path = os.path.join(directory_path, file_name)
            mark_file_name = file_name.replace("_index.csv", ".csv")
            mark_file_path = os.path.join(directory_path, mark_file_name)
            print("Processing file {} out of {}".format(file_counter, num_files))
            attach_column(mark_file_path, index_file_path)
            file_counter += 1