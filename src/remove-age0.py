import pandas as pd
import os


def remove_age0(infile_path):
    # print(infile_path)
    points = pd.read_csv(infile_path)
    # print(points)
    age0_removed_df = points[points['6'] != 0]
    outfile_path = infile_path.replace('.csv', '_age0removed.csv')
    age0_removed_df.to_csv(outfile_path, index=False)


directory_path = '/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output/mm5'
files = [f for f in os.listdir(directory_path) if f.lower().endswith('_index_path_hopvec.csv') and os.path.isfile(os.path.join(directory_path, f))]

# Iterate over each file
file_counter = 1
num_files = len(files)
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    print("Removing age 0 from file {} out of {}".format(file_counter, num_files))
    remove_age0(file_path)
    file_counter += 1
