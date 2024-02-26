import pandas as pd
from math import comb

def xnor(a, b):
    return (a == b)


def find_frac_onehop_neighbors(pivot, points: pd.DataFrame):
    """
    Assumes the input pivot point is of shape <Ind_TBi, Ind_Ri, Ind_TBj, Ind_Rj, Ind_Ok>
    """
    num_localmins = 0
    num_nonmins = 0
    total_reducer = 0
    pivot_dims = len(pivot) - 1 # ignore the time column
    num_ans = (comb(pivot_dims, 1) * pow(2, 1))/2 
    for d in range(pivot_dims):
        poten_bottom_neighbor_conf = pivot.copy()
        poten_bottom_neighbor_conf[d] -= 1
        poten_bottom_neighbor_conf = poten_bottom_neighbor_conf[:-1]
        poten_top_neighbor_conf = pivot.copy()
        poten_top_neighbor_conf[d] += 1
        poten_top_neighbor_conf = poten_top_neighbor_conf[:-1]
        assert len(poten_bottom_neighbor_conf) == len(poten_top_neighbor_conf) and len(poten_top_neighbor_conf) == pivot_dims, \
                    "The dimension of pivot point and generated candidates don't match."
        #points[(points["Age"] >= 35) & (points["Age"] <= 40) & (points[""])]
        condition_bot = (
            (points.iloc[:, 0] == poten_bottom_neighbor_conf[0]) &
            (points.iloc[:, 1] == poten_bottom_neighbor_conf[1]) &
            (points.iloc[:, 2] == poten_bottom_neighbor_conf[2]) &
            (points.iloc[:, 3] == poten_bottom_neighbor_conf[3]) &
            (points.iloc[:, 4] == poten_bottom_neighbor_conf[4])
        )
        matched_bottom_points = points[condition_bot]
        condition_top = (
            (points.iloc[:, 0] == poten_top_neighbor_conf[0]) &
            (points.iloc[:, 1] == poten_top_neighbor_conf[1]) &
            (points.iloc[:, 2] == poten_top_neighbor_conf[2]) &
            (points.iloc[:, 3] == poten_top_neighbor_conf[3]) &
            (points.iloc[:, 4] == poten_top_neighbor_conf[4])
        )
        matched_top_points = points[condition_top]
        if matched_bottom_points.empty or matched_top_points.empty:
            print("Either one or both potential candidates for this dimension of the pivot do NOT exist in the given points.")
            total_reducer += 1
        else:
            if matched_bottom_points.shape[0] > 1:
                # one_matched_bot = matched_bottom_points.groupby(matched_bottom_points.columns[0, 1, 2, 3, 4]).columns[5].mean().reset_index()
                average_time = matched_bottom_points[matched_bottom_points.columns[5]].mean()
                matched_bottom_points = matched_bottom_points.iloc[[0]]
                matched_bottom_points[matched_bottom_points.columns[5]] = average_time
                assert matched_bottom_points.shape[0] == 1, "There is bug in groupby bottom."
            if matched_top_points.shape[0] > 1:
                # one_matched_top = matched_top_points.groupby(matched_top_points.columns[0, 1, 2, 3, 4]).columns[5].mean().reset_index()
                average_time = matched_top_points[matched_top_points.columns[5]].mean()
                matched_top_points = matched_top_points.iloc[[0]]
                matched_top_points[matched_top_points.columns[5]] = average_time
                assert matched_top_points.shape[0] == 1, "There is bug in groupby top."
            # run calculation now
            bottom_is_better = matched_bottom_points.columns[5] > pivot[5]
            top_is_better = matched_top_points.columns[5] > pivot[5]
            directions_match = xnor(bottom_is_better, top_is_better)
            if directions_match:
                # this is a local minima
                num_localmins += 1
            else:
                num_nonmins += 1
    divisor = (num_ans - total_reducer)
    print("divisor: ", divisor)
    print("nonmins: ", num_nonmins)
    print("localmins: ", num_localmins)
    if divisor < 1:
        frac = -1
    else:
        frac = float(num_nonmins)/divisor
    return frac
    


def main():
    '''
    bottom_is_better = matched_bottom_points["perf"] > pivot[5]
    top_is_better = matched_top_points["perf"] > pivot[5]
    directions_match = xnor(bottom_is_better, top_is_better)
    if directions_match:
        print("z")
    '''
    file_path = 'measuredpoints.csv'
    index_based_df = pd.read_csv(file_path, header=None)
    row = index_based_df.iloc[1].tolist()
    #print(index_based_df)
    print(row)
    print(find_frac_onehop_neighbors(row, index_based_df))
    #index_based_df['frac'] = index_based_df.apply(find_frac_onehop_neighbors, args=(index_based_df), axis=1)
    #index_based_df.to_csv('fracadded.csv', index=False)
    #for all rows:
        #1hop column<< find_frac_onehop_neighbors()


if __name__ == "__main__":
    main()