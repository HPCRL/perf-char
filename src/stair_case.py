import os
import sys
import pandas as pd
from myutils import make_bot_top, compare_three



unique_5hop_min = {}
def process_file(infile_path):
    index_based_df = pd.read_csv(infile_path, header=None)
   
    # create a df only containing the first rows that the age (at column 6) changes
    path_points_df = index_based_df[index_based_df.iloc[:, 6].diff() != 0].copy()
    last_point= path_points_df.tail(1)
    # print(type(last_point))
    
    config = tuple(last_point.iloc[:, 0:5].values.flatten().tolist())
    vect = last_point.iloc[:, -5:].values.flatten().tolist()

    if vect != ['1']*5:
        print("ERROR, final point must be a 5hop local min!!") 
    else:
        if config not in unique_5hop_min:
            unique_5hop_min[config] = 1
            print(infile_path)
            print(config)
            print("hit unique 5 hop min", unique_5hop_min)
        else:
            unique_5hop_min[config] += 1

        # print(config)
        # print(vect)
        # print(path_points_df.tail(1))
    
    return len(unique_5hop_min.keys())
    
import matplotlib.pyplot as plt
def draw_line_chart(x_values, y_values):
    plt.figure(figsize=(12, 6))
    # Create a line chart
    plt.plot(x_values, y_values, label='Stair Chart')

    # Add labels and title
    plt.xlabel('File number')
    plt.ylabel('# of uniq 5 hop')
    # plt.xticks(x_values)
    plt.xticks(x_values[::10])
    
    # Add a legend (optional)
    plt.legend()

    # Show the chart
    plt.show()
    plt.savefig('stair.pdf')



figure_x = []
figure_y = []

def main():
    if len(sys.argv) != 2:
        print("Usage: python stair_case.py <path_to_folder_with_wmts_eachhop_csvs>")
    else:
        directory_path = sys.argv[1]
        # directory_path = '/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output/mm5'
        # directory_path = '/media/datassd/shared/space_char/perf-char-scripts_yufantest/Characterization_data/_output'
        # directory_path = '/media/datassd/sina/perf-characterization/data/pz5-merged200'
        files = [f for f in os.listdir(directory_path) if f.lower().endswith('_index_wmts_path_eachhop.csv') and os.path.isfile(os.path.join(directory_path, f))]

        # Iterate over each file
        file_counter = 1
        num_files = len(files)
        print("num_files:", num_files)
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            print("Processing file {} out of {}".format(file_counter, num_files))
            count = process_file(file_path)
            print("5hop count ", count)
            figure_y.append(count)
            figure_x.append(file_counter)
            file_counter += 1
        
        assert(len(figure_x) == len(figure_y))
        draw_line_chart(figure_x, figure_y)



if __name__ == "__main__":
    main()
