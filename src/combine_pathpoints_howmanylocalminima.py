import pandas as pd
import os


#input_path = '/media/datassd/sina/perf-characterization/data/_output'
# input_path = '/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output/mm5'
input_path = '/media/datassd/sina/perf-characterization/chendi-repo/Characterization_data/_output/'
output_file = '/media/datassd/sina/perf-characterization/myoutputs/merged_pathpoints_howmanylocalminima_mm3_50_tsbased_lastone_combkey.csv'



csv_files = [file for file in os.listdir(input_path) if file.endswith('_wmts_path_eachhop.csv')]

unique_configs = set()

dfs = []
num_repeated = 0
# Loop through each CSV file and process its data
for file in csv_files:
    file_path = os.path.join(input_path, file)
    df = pd.read_csv(file_path)
    
    # Iterate through rows and add unique configurations to the set
    for index, row in df.iterrows():
        config_key = (tuple(row[8]), row[9], row[10], row[11], row[12], row[13]) # get the tile size as the config (I have to change this row[8] is being deprecated)
        if config_key not in unique_configs:
            unique_configs.add(config_key)
            dfs.append(row)
        else:
            num_repeated += 1
            old_config = df.loc[df.iloc[:, :5].eq(row[:5]).all(axis=1), df.columns[-5:]].iloc[-1]
            new_config = row[-5:].astype(int)
            if not old_config.equals(new_config):
                print(f"Repetitive Row {config_key} - Old Config: {old_config.tolist()}, New Config: {new_config.tolist()}")
print("num of repeated configs: ", num_repeated)



# need this to keep data types:
dtypes = {col: df[col].dtype for col in df.columns}


# Create a DataFrame from the list of unique rows
# merged_df = pd.DataFrame(dfs, columns=df.columns, dtype=object) #only using this makes all columns float
merged_df = pd.DataFrame(dfs, columns=df.columns).astype(dtypes)

# add a column at end to show the last 'one' value's nhop
last_five_columns = merged_df.iloc[:, -5:]
# merged_df['last_1'] = last_five_columns.apply(lambda row: row.idxmax() if 1 in row.values else None, axis=1)
merged_df['last_1'] = last_five_columns.apply(lambda row: row[::-1].index[row[::-1].eq(1)][0] if 1 in row.values else None, axis=1)
# merged_df['last_one'] = merged_df.apply(lambda row: row[::-1].idxmax(), axis=1)

# Remove 1e+10
#merged_df = merged_df[merged_df.iloc[:, 5] < 1e+9]

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(output_file, index=False)