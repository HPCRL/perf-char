import os
import pandas as pd
import matplotlib.pyplot as plt
import sys


def process_csv_file(file_path, numOps):
    df = pd.read_csv(file_path)
    sixth_column_value = df.iloc[0, 1]  # Assuming 0-indexed, change if your data is 1-indexed
    gflops = 1.0e-9 * numOps / sixth_column_value
    return gflops


def process_csv_file_for_remove_dup(file_path):
    df = pd.read_csv(file_path)
    return df.iloc[0]


if len(sys.argv) != 6:
    print("Usage: python histogram_random_points.py <path_to_index_based_csvs_folder> <mm m> <mm n> <mm k>")
else:
    folder_path = sys.argv[1]
    m = int(sys.argv[2])
    n = int(sys.argv[3])
    k = int(sys.argv[4])
    remove_dups = False
    if sys.argv[5].lower() == "true":
        remove_dups = True
    
    numOps = 2 * m * n * k
    
    if remove_dups == False:
        values = []

        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                value = process_csv_file(file_path, numOps)
                values.append(value)
        print("Number of points before duplicate removal: ", len(values))
        max_value = max(values)
        num_bins = 10
        bins = [max_value * i / num_bins for i in range(num_bins + 1)]

        myn, bins, patches = plt.hist(values, bins=bins, edgecolor='black', alpha=0.7)
        for i in range(10):
            if myn[i] > 0:
                plt.text(bins[i] + 190, myn[i] + 1, str(int(myn[i])), fontsize=11, ha='center', va='bottom')
        plt.xlabel('GFLOPS')
        plt.ylabel('Frequency')
        plt.title('Distribution of GFLOPS Values')
        plt.savefig('hist.pdf')

    elif remove_dups == True:
        all_first_rows = []

        # Collect all first rows
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                first_row = process_csv_file_for_remove_dup(file_path)
                all_first_rows.append(first_row)

        all_first_rows_df = pd.concat(all_first_rows, axis=1, ignore_index=True).T
        # Make the rows unique based on "tile_sizes"
        # print(all_first_rows_df)
        # print(all_first_rows_df.iloc[0, 2])
        all_first_rows_unique = all_first_rows_df.drop_duplicates(subset='tile_sizes')
        print("Number of points after duplicate removal: ", len(all_first_rows_unique))

        # Apply the transformation and collect values
        values = []
        for index, row in all_first_rows_unique.iterrows():
            sixth_column_value = row.iloc[1]  # Assuming 0-indexed, change if your data is 1-indexed
            gflops = 1.0e-9 * numOps / sixth_column_value
            values.append(gflops)

        # Find the maximum value and create bins
        max_value = max(values)
        num_bins = 10
        bins = [max_value * i / num_bins for i in range(num_bins + 1)]

        # Plot the bar chart
        myn, bins, patches = plt.hist(values, bins=bins, edgecolor='black', alpha=0.7)
        for i in range(10):
            if myn[i] > 0:
                plt.text(bins[i] + 190, myn[i] + 1, str(int(myn[i])), fontsize=11, ha='center', va='bottom')
        plt.xlabel('GFLOPS')
        plt.ylabel('Frequency')
        plt.title('Distribution of GFLOPS Values')
        plt.savefig('hist_noDups.pdf')