import pandas as pd
import os


input_directory = '/media/datassd/sina/perf-characterization/data/_output'

output_file = '/media/datassd/sina/perf-characterization/myoutputs/merged_outputs_old.csv'

dataframes = []

# Loop through each CSV file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('_updated_frac_added.csv'):
        file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(file_path)
        dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)

# Group by the first five columns and calculate the mean of the 6th column
result_df = merged_df.groupby(merged_df.columns[:5].tolist())[5].mean().reset_index()

result_df.to_csv(output_file, index=False)
print("Merged and averaged data saved to:", output_file)