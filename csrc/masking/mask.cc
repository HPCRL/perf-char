#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

void generateMasksRecursively(int dims, std::vector<int>& mask, const std::vector<int>& chosen_dims, 
                              std::vector<std::vector<int>>& masks, int index = 0) {
    if (index == chosen_dims.size()) {
        // end of the chosen_dims, add to masks
        masks.push_back(mask);
        return;
    }

    // set current chosen_dims to -1/1

    mask[chosen_dims[index]] = -1;
    generateMasksRecursively(dims, mask, chosen_dims, masks, index + 1);

    mask[chosen_dims[index]] = 1;
    generateMasksRecursively(dims, mask, chosen_dims, masks, index + 1);
}

void generateMasks(int dims, const std::vector<int>& chosen_dims, std::vector<std::vector<int>>& masks) {
    std::vector<int> mask(dims, 0); // 0 means not chosen

    // change selected dimensions to 1/-1
    generateMasksRecursively(dims, mask, chosen_dims, masks);
}

std::vector<int> getRemainingDims(int total_dims, const std::vector<int>& exclude_dims) {
    std::vector<int> remaining_dims;
    for (int i = 0; i < total_dims; ++i) {
        if (std::find(exclude_dims.begin(), exclude_dims.end(), i) == exclude_dims.end()) {
            remaining_dims.push_back(i);
        }
    }
    return remaining_dims;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: ./mask <total_dims> <num_hops>" << std::endl;
        return 1;
    }

    // example: 5 for matmul
    // 2 hops
    int total_dims = std::stoi(argv[1]);
    int num_hops = std::stoi(argv[2]);

    // you can use exclude_dims to exclude some dimensions
    // for example in Conv2d, B=1, you won't need to generate masks for B
    // because B dimension only has 1 in factors list
    std::vector<int> exclude_dims = {}; 

    std::vector<int> remaining_dims = getRemainingDims(total_dims, exclude_dims);

    // std::cout << "Remaining dims: "; // test 0 1 2 3 4
    // for (int num : remaining_dims) {
    //     std::cout << num << "\t";
    // }
    // std::cout << std::endl;

    // use dimensions get all possible combinations of 1 and 0 in do-while loop
    // indicate which dimensions to change
    std::vector<int> dimensions(remaining_dims.size(), 0);
    std::fill(dimensions.end() - num_hops, dimensions.end(), 1);

    std::vector<std::vector<int>> masks;

    do {
        // chosen_dims used to store the dimensions that need to change
        std::vector<int> chosen_dims;
        for (int i = 0; i < remaining_dims.size(); ++i) {
            if (dimensions[i] == 1) {
                chosen_dims.push_back(remaining_dims[i]);
            }
        }

        generateMasks(total_dims, chosen_dims, masks);

    } while (std::next_permutation(dimensions.begin(), dimensions.end()));
    /*
    for (const auto& mask : masks) {
        for (int num : mask) {
            std::cout << num << ",";
        }
        std::cout << std::endl;
    }
    */
    for (const auto& mask : masks) {
        bool first = true;
        for (int num : mask) {
        if (!first) {
            std::cout << ",";
        }
        std::cout << num;
        first = false;
        }
        std::cout << std::endl;
    }
    //std::cout << "Total masks: " << masks.size() << std::endl;

    return 0;
}