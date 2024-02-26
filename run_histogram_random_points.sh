input_json_folder=$1 #"data/input_jsons"
pz_m=$2
pz_n=$3
pz_k=$4
reduc_dim=$5
mm_testcase=$6
num_start=$7

source ../myenv/bin/activate
echo "Python from:"
which python

python src/extract_tiles.py $input_json_folder
#cd csrc/factoring/
#make
#cd ../../

# ./factor M N K num_reduction_dim testcase num_start_points
#./factor 512 64 768 1 3 50
#./factor 512 3072 768 1 4 15
#./factor 512 768 3072 1 5 15
# csrc/factoring/factor $pz_m $pz_n $pz_k $reduc_dim $mm_testcase $num_start

# Works with the non-indexed csv files:
python src/histogram_random_points.py data/_output $pz_m $pz_n $pz_k False
python src/histogram_random_points.py data/_output $pz_m $pz_n $pz_k True
mkdir data/_output/results
mv hist.pdf data/_output/results/
mv hist_noDups.pdf data/_output/results/
mv "data/_output" "data/hist_mm${mm_testcase}_numstart${num_start}_output"