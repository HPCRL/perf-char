#!/bin/bash

####
# This is a script to run the whole characterization processing on a folder containing the json logs from ansor.
####

if [ "$#" -lt 7 ]; then
    echo "Error: Insufficient number of arguments. Please provide at least 7 arguments."
    echo "Usage: $0 <json_folder> <pz_m> <pz_n> <pz_k> <num_reduction_dim> <mm_testcase_num> <num_start_points>"
    exit 1
fi

#### mask generation:
cd csrc/masking/
make
cd ../../
csrc/masking/mask 5 1 > assets/onehop_masks.csv
csrc/masking/mask 5 2 > assets/twohop_masks.csv
csrc/masking/mask 5 3 > assets/threehop_masks.csv
csrc/masking/mask 5 4 > assets/fourhop_masks.csv
csrc/masking/mask 5 5 > assets/fivehop_masks.csv


# echo "Script name: $0"
# echo "Total number of arguments: $#"
# echo "All arguments: $@"
# echo "First argument: $1"
# echo "Second argument: $2"

# New Workflow:
input_json_folder=$1 #"data/input_jsons"
pz_m=$2
pz_n=$3
pz_k=$4
reduc_dim=$5
mm_testcase=$6
num_start=$7
input_json_folder2=$8
num_start2=$9

source ../myenv/bin/activate
echo "Python from:"
which python

python src/extract_tiles.py $input_json_folder
cd csrc/factoring/
make
cd ../../
# ./factor M N K num_reduction_dim testcase num_start_points
#./factor 512 64 768 1 3 50
#./factor 512 3072 768 1 4 15
#./factor 512 768 3072 1 5 15
csrc/factoring/factor $pz_m $pz_n $pz_k $reduc_dim $mm_testcase $num_start

python src/merge_two_folders.py <path_folder1> <path_folder2> <merged_output_folder>
python src/remove_dup_starts.py <input_folder> <output_folder>
python src/attach_mark_to_indexbased.py data/_output
python src/eachhopminima.py data/_output
python src/stair_case.py data/_output
mkdir data/_output/results
mv stair.pdf data/_output/results/
mv "data/_output" "data/mm${mm_testcase}_numstart${num_start}_output"