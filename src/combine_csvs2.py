import pandas as pd
import os


#input_path = '/media/datassd/sina/perf-characterization/data/_output'
input_path = '/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output/mm5'
output_file = '/media/datassd/sina/perf-characterization/myoutputs/merged_pathes_hopvec_mm5_15.csv'


csv_files = [file for file in os.listdir(input_path) if file.endswith('_path_hopvec_age0removed.csv')]

unique_configs = set()

dfs = []

# Loop through each CSV file and process its data
for file in csv_files:
    file_path = os.path.join(input_path, file)
    df = pd.read_csv(file_path)
    
    # Iterate through rows and add unique configurations to the set
    for index, row in df.iterrows():
        config_key = tuple(row[:5])  # Exclude the last three column (time, frac1, frac2)
        if config_key not in unique_configs:
            unique_configs.add(config_key)
            dfs.append(row)

# Create a DataFrame from the list of unique rows
merged_df = pd.DataFrame(dfs, columns=df.columns)
# Remove 1e+10
merged_df = merged_df[merged_df.iloc[:, 5] < 1e+9]

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(output_file, index=False)