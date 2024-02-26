import pandas as pd
from math import comb
import os

def xnor(a, b):
    return (a == b)


def compare_three(pivot, bot, top, points: pd.DataFrame):
    ignore = 0
    localmin = 0
    nonmin = 0
    bot_conf = bot
    top_conf = top
    condition_bot = (
            (points.iloc[:, 0] == bot_conf[0]) &
            (points.iloc[:, 1] == bot_conf[1]) &
            (points.iloc[:, 2] == bot_conf[2]) &
            (points.iloc[:, 3] == bot_conf[3]) &
            (points.iloc[:, 4] == bot_conf[4])
    )
    matched_bot_points = points[condition_bot]
    condition_top = (
        (points.iloc[:, 0] == top_conf[0]) &
        (points.iloc[:, 1] == top_conf[1]) &
        (points.iloc[:, 2] == top_conf[2]) &
        (points.iloc[:, 3] == top_conf[3]) &
        (points.iloc[:, 4] == top_conf[4])
    )
    matched_top_points = points[condition_top]

    if matched_bot_points.shape[0] > 1:
        # print("more than one bot found")
        # one_matched_bot = matched_bottom_points.groupby(matched_bottom_points.columns[0, 1, 2, 3, 4]).columns[5].mean().reset_index()
        average_time = matched_bot_points[matched_bot_points.columns[5]].mean()
        matched_bot_points = matched_bot_points.iloc[[0]]
        matched_bot_points[matched_bot_points.columns[5]] = average_time
        assert matched_bot_points.shape[0] == 1, "There is bug in averaging bottom matches."
    if matched_top_points.shape[0] > 1:
        # print("more than one top found")
        # one_matched_top = matched_top_points.groupby(matched_top_points.columns[0, 1, 2, 3, 4]).columns[5].mean().reset_index()
        average_time = matched_top_points[matched_top_points.columns[5]].mean()
        matched_top_points = matched_top_points.iloc[[0]]
        matched_top_points[matched_top_points.columns[5]] = average_time
        assert matched_top_points.shape[0] == 1, "There is bug in averaging top matches."

    if matched_bot_points.empty or matched_top_points.empty or (pivot[5] > 1e+9):
        #print("Either one or both potential candidates for this dimension of the pivot do NOT exist in the given points.")
        ignore = 1
    else:
        bot_time = matched_bot_points[matched_bot_points.columns[5]].iloc[0]
        top_time = matched_top_points[matched_top_points.columns[5]].iloc[0]
        if (bot_time > 1e+9) or (top_time > 1e+9):
            ignore = 1
        else:
            bot_is_worse = bot_time > pivot[5]
            top_is_worse = top_time > pivot[5]
            directions_match = xnor(bot_is_worse, top_is_worse)
            if directions_match:
                # this is a local minima/maxima
                localmin = 1
            else:
                nonmin = 1
    return ignore, localmin, nonmin


def sum_lists(list1, list2):
    result = []
    for elem1, elem2 in zip(list1, list2):
        result.append(elem1 + elem2)
    return result


def make_bot_top(pivot, mask1, mask2):
    bot = sum_lists(pivot[:5], mask1)
    top = sum_lists(pivot[:5], mask2)
    return bot, top


def calculate_row_frac(pivot, points: pd.DataFrame, masks_df: pd.DataFrame, nhop: int, nfeatures: int):
    """
    Assumes the input pivot point is of shape <Ind_TBi, Ind_Ri, Ind_TBj, Ind_Rj, Ind_Ko>
    """
    # next line works if we want to convert the pivot to list and based on my testing it should be ok
    # pivot = pivot.tolist()
    pivot_neighbor_points = points[points[6] == pivot[6]]
    # print("roundCounter\n", pivot_neighbor_points)

    reducer, num_localmins, num_nonmins = 0, 0, 0
    
    for i in range(0, len(masks_df), 2):
        # print("{}th up and down masks".format(i))
        mask1 = masks_df.iloc[i].tolist()
        mask2 = masks_df.iloc[i+1].tolist()
        bot, top = make_bot_top(pivot, mask1, mask2)
        ignore, localmins, nonmins = compare_three(pivot, bot, top, pivot_neighbor_points)
        reducer += ignore
        num_localmins += localmins
        num_nonmins += nonmins
    
    pivot_dims = nfeatures # only care about the feature dimensions in calculating the num of max possible answers (pairs)
    num_ans = (comb(pivot_dims, nhop) * pow(2, nhop))/2
    divisor = (num_ans - reducer)
    
    # print("reducer: ", reducer)
    # print("divisor: ", divisor)
    # print("nonmins: ", num_nonmins)
    # print("localmins: ", num_localmins)
    
    if divisor < 1:
        frac = -1
    else:
        frac = float(num_nonmins)/divisor
    return frac
    
    

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
    
    path_points_df['1hop_frac'] = path_points_df.apply(calculate_row_frac, args=(index_based_df, onehop_masks_df, 1, 5), axis=1)
    path_points_df['2hop_frac'] = path_points_df.apply(calculate_row_frac, args=(index_based_df, twohop_masks_df, 2, 5), axis=1) 
    
    outfile_path = infile_path.replace('.csv', '_path_frac_added_2hoponly.csv')
    path_points_df.to_csv(outfile_path, index=False)
    


def main():
    # measured_file = "/media/datassd/sina/perf-characterization/proj/measuredpoints2.csv"
    # process_file(measured_file)
    
    
    #directory_path = "/media/datassd/sina/perf-characterization/data/_output"
    directory_path = "/media/datassd/sina/perf-characterization/gitdata/Characterization_data/_output"
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
