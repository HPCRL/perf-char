import pandas as pd
from math import comb
import os
from myutils import sum_lists, xnor, make_bot_top, compare_three



def calculate_row_vector(pivot, points: pd.DataFrame, masks_df: pd.DataFrame, nhop: int, nfeatures: int):
    """
    Assumes the input pivot point is of shape <Ind_TBi, Ind_Ri, Ind_TBj, Ind_Rj, Ind_Ko>
    """
    # next line works if we want to convert the pivot to list and based on my testing it should be ok
    # pivot = pivot.tolist()
    pivot_neighbor_points = points[points[6] == pivot[6]]
    # print("roundCounter\n", pivot_neighbor_points)

    localmin_vector = []
    
    for i in range(0, len(masks_df), 2):
        # print("{}th up and down masks".format(i))
        mask1 = masks_df.iloc[i].tolist()
        mask2 = masks_df.iloc[i+1].tolist()
        bot, top = make_bot_top(pivot, mask1, mask2)
        localmin, _, _ = compare_three(pivot, bot, top, pivot_neighbor_points)
        localmin_vector.append(localmin)
    
    pivot_dims = nfeatures # only care about the feature dimensions in calculating the num of max possible answers (pairs)
    num_ans = (comb(pivot_dims, nhop) * pow(2, nhop))/2
    assert num_ans == len(localmin_vector), "length of the localmin vector does not match with the number of expected answers"
    
    return localmin_vector 
    
    
def process_file(infile_path):
    index_based_df = pd.read_csv(infile_path, header=None)
    onehop_masks_path = 'onehop_masks.csv'
    onehop_masks_df = pd.read_csv(onehop_masks_path, header=None)
    twohop_masks_path = 'twohop_masks.csv'
    twohop_masks_df = pd.read_csv(twohop_masks_path, header=None)
    
    # create a df only containing the first rows that the age (at column 6) changes
    path_points_df = index_based_df[index_based_df.iloc[:, 6].diff() != 0].copy()
    
    # no need to do next line (commented) since we already have access to the row's age column in the calculate_row_frac func
    # path_points_df.apply(lambda row: calculate_row_frac(row, index_based_df, onehop_masks_df, 1), axis=1)

    # no where I explicitly convert the pivot to a list, and it is a df with one each time that apply uses it
    # maybe I should explicitly make it to be a list to avoid possible problems later
    # I tested this at the beginning of the calculate_row_frac function and it seems not to matter if its a list or not
    
    path_points_df['1hop_vec'] = path_points_df.apply(calculate_row_vector, args=(index_based_df, onehop_masks_df, 1, 5), axis=1)
    path_points_df['2hop_vec'] = path_points_df.apply(calculate_row_vector, args=(index_based_df, twohop_masks_df, 2, 5), axis=1) 
    
    expanded_1hop_path_points_df = path_points_df['1hop_vec'].apply(pd.Series)
    expanded_1hop_path_points_df = expanded_1hop_path_points_df.rename(columns=lambda x: f'1hopvec_{x}')
    
    expanded_2hop_path_points_df = path_points_df['2hop_vec'].apply(pd.Series)
    expanded_2hop_path_points_df = expanded_2hop_path_points_df.rename(columns=lambda x: f'2hopvec_{x}')
    # Concatenate the new columns to the original DataFrame
    expanded_path_points_df = pd.concat([path_points_df, expanded_1hop_path_points_df], axis=1).drop('1hop_vec', axis=1)
    expanded_path_points_df = pd.concat([expanded_path_points_df, expanded_2hop_path_points_df], axis=1).drop('2hop_vec', axis=1)
    
    outfile_path = infile_path.replace('.csv', '_path_hopvec.csv')
    #outfile_pathtest = infile_path.replace('.csv', '_path_hopvec_test.csv')
    #path_points_df.to_csv(outfile_pathtest, index=False)
    expanded_path_points_df.to_csv(outfile_path, index=False)
    

def main():
    #measured_file = "/media/datassd/sina/perf-characterization/proj/new_measuredpoints.csv"
    #process_file(measured_file)
    
    # directory_path = "/media/datassd/sina/perf-characterization/data/_output"
    # directory_path = "/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output"
    directory_path = '/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output/mm5'
    files = [f for f in os.listdir(directory_path) if f.lower().endswith('_index.csv') and os.path.isfile(os.path.join(directory_path, f))]

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
