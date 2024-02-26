import os
import sys
import pandas as pd
from myutils import make_bot_top, compare_three


def find_highest_mark(neighbour_points: pd.DataFrame):
    max_rank = neighbour_points[7].max()
    return max_rank


def calculate_thishopmin(pivot, points: pd.DataFrame, masks_df: pd.DataFrame, nhop: int):
    # filter and keep the points only with the same age:
    pivot_neighbor_points = points[points[6] == pivot[6]]
    thishopmin = 0
    
    highest_mark = find_highest_mark(pivot_neighbor_points)
    if nhop > highest_mark:
        return -1
    
    localmin_vector = []
    for i in range(0, len(masks_df), 2):
        # print("{}th up and down masks".format(i))
        mask1 = masks_df.iloc[i].tolist()
        mask2 = masks_df.iloc[i+1].tolist()
        bot, top = make_bot_top(pivot, mask1, mask2)
        localmin, _, _ = compare_three(pivot, bot, top, pivot_neighbor_points)
        localmin_vector.append(localmin)
    if sum(localmin_vector) == len(localmin_vector):
        # I am a local min with respect to this hop overall
        thishopmin = 1
    return thishopmin



def process_file(infile_path):
    
    index_based_df = pd.read_csv(infile_path, header=None)
    onehop_masks_path = 'assets/onehop_masks.csv'
    twohop_masks_path = 'assets/twohop_masks.csv'
    threehop_masks_path = 'assets/threehop_masks.csv'
    fourhop_masks_path = 'assets/fourhop_masks.csv'
    fivehop_masks_path = 'assets/fivehop_masks.csv'
    onehop_masks_df = pd.read_csv(onehop_masks_path, header=None)
    twohop_masks_df = pd.read_csv(twohop_masks_path, header=None)
    threehop_masks_df = pd.read_csv(threehop_masks_path, header=None)
    fourhop_masks_df = pd.read_csv(fourhop_masks_path, header=None)
    fivehop_masks_df = pd.read_csv(fivehop_masks_path, header=None)
    
    # create a df only containing the first rows that the age (at column 6) changes
    path_points_df = index_based_df[index_based_df.iloc[:, 6].diff() != 0].copy()
    
    # no need to do next line (commented) since we already have access to the row's age column in the calculate_row_frac func
    # path_points_df.apply(lambda row: calculate_row_frac(row, index_based_df, onehop_masks_df, 1), axis=1)

    # no where I explicitly convert the pivot to a list, and it is a df with one each time that apply uses it
    # maybe I should explicitly make it to be a list to avoid possible problems later
    # I tested this at the beginning of the calculate_row_frac function and it seems not to matter if its a list or not
    

    #new developement
    path_points_df['1h_min'] = path_points_df.apply(calculate_thishopmin, args=(index_based_df, onehop_masks_df, 1), axis=1)
    path_points_df['2h_min'] = path_points_df.apply(calculate_thishopmin, args=(index_based_df, twohop_masks_df, 2), axis=1)
    path_points_df['3h_min'] = path_points_df.apply(calculate_thishopmin, args=(index_based_df, threehop_masks_df, 3), axis=1)
    path_points_df['4h_min'] = path_points_df.apply(calculate_thishopmin, args=(index_based_df, fourhop_masks_df, 4), axis=1)
    path_points_df['5h_min'] = path_points_df.apply(calculate_thishopmin, args=(index_based_df, fivehop_masks_df, 5), axis=1)


    # path_points_df['1hop_vec'] = path_points_df.apply(calculate_row_vector, args=(index_based_df, onehop_masks_df, 1, 5), axis=1)
    # path_points_df['2hop_vec'] = path_points_df.apply(calculate_row_vector, args=(index_based_df, twohop_masks_df, 2, 5), axis=1) 
    
    # expanded_1hop_path_points_df = path_points_df['1hop_vec'].apply(pd.Series)
    # expanded_1hop_path_points_df = expanded_1hop_path_points_df.rename(columns=lambda x: f'1hopvec_{x}')
    
    # expanded_2hop_path_points_df = path_points_df['2hop_vec'].apply(pd.Series)
    # expanded_2hop_path_points_df = expanded_2hop_path_points_df.rename(columns=lambda x: f'2hopvec_{x}')
    
    # Concatenate the new columns to the original DataFrame
    # expanded_path_points_df = pd.concat([path_points_df, expanded_1hop_path_points_df], axis=1).drop('1hop_vec', axis=1)
    # expanded_path_points_df = pd.concat([expanded_path_points_df, expanded_2hop_path_points_df], axis=1).drop('2hop_vec', axis=1)
    
    outfile_path = infile_path.replace('.csv', '_path_eachhop.csv')
    path_points_df.to_csv(outfile_path, index=False)



def main():
    if len(sys.argv) != 2:
        print("Usage: python eachhopminima.py <path_to_index_based_csvs_folder_with_mark_attached>")
    else:
        directory_path = sys.argv[1]
        # directory_path = '/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output/mm5'
        # directory_path = '/media/datassd/sina/perf-characterization/chendi-repo/Characterization_data/_output'
        # directory_path = '/media/datassd/sina/perf-characterization/data/pz5-merged200'
        files = [f for f in os.listdir(directory_path) if f.lower().endswith('_index_wmts.csv') and os.path.isfile(os.path.join(directory_path, f))]

        # Iterate over each file
        file_counter = 1
        num_files = len(files)
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            print("Processing file {} out of {}".format(file_counter, num_files))
            process_file(file_path)
            file_counter += 1


if __name__ == "__main__":
    main()
