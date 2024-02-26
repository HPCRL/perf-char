#include <math.h>
#include <algorithm>
#include <iostream>
#include <limits>
#include <sstream>
#include <tuple>
#include <unordered_map>
#include <vector>
#include <fstream>

using QueryKey = std::tuple<int, int, int>;
using Integer = int;
const int INT_MAX = std::numeric_limits<int>::max();

struct key_hash : public std::unary_function<QueryKey, std::size_t> {
  std::size_t operator()(const QueryKey& k) const {
    return std::get<0>(k) ^ std::get<1>(k) ^ std::get<2>(k);
  }
};

class SplitFactorizationMemo {
 public:
  const std::vector<std::vector<Integer>>& GetFactorizationSchemes(int extent, int n_lengths,
                                                                   int max_innermost_factor);
  const std::vector<int>& GetFactors(int n);

 private:
  void DfsEnum_reducerate(int now, int remaining_length, int max_innermost_factor);

  std::unordered_map<QueryKey, std::vector<std::vector<Integer>>, key_hash> memory_;

  int n_lengths_;
  std::vector<Integer> tmp_stack_;
  std::vector<std::vector<Integer>>* results_;
  std::unordered_map<int, std::vector<int>> factor_memory_;
};

const std::vector<std::vector<Integer>>& SplitFactorizationMemo::GetFactorizationSchemes(
    int extent, int n_lengths, int max_innermost_factor) {
  QueryKey key = std::make_tuple(extent, n_lengths, max_innermost_factor);
  const auto& it = memory_.find(key);
  if (it != memory_.end()) {
    return it->second;
  }

  tmp_stack_ = std::vector<Integer>(n_lengths, Integer());
  results_ = &memory_[key];
  n_lengths_ = n_lengths;

  DfsEnum_reducerate(0, extent, max_innermost_factor);

  return *results_;
}

void SplitFactorizationMemo::DfsEnum_reducerate(int now, int remaining_length,
                                                int max_innermost_factor) {
  if (now == n_lengths_) {
    if (tmp_stack_.back() <= max_innermost_factor) {
      results_->push_back(tmp_stack_);
    }
  } else {
    for (const auto& f : GetFactors(remaining_length)) {
      tmp_stack_[now] = Integer(f);
      DfsEnum_reducerate(now + 1, remaining_length / f, max_innermost_factor);
    }
  }
}

const std::vector<int>& SplitFactorizationMemo::GetFactors(int n) {
  auto it = factor_memory_.find(n);
  if (it != factor_memory_.end()) {
    return it->second;
  }

  std::vector<int>& res = factor_memory_[n];
  int step = n % 2 == 0 ? 1 : 2;
  for (size_t i = 1; i < static_cast<size_t>(std::sqrt(n)) + 1; i += step) {
    if (n % i == 0) {
      res.push_back(i);
      if (n / i != i) {
        res.push_back(n / i);
      }
    }
  }
  std::sort(res.begin(), res.end());
  return res;
}

std::vector<int> string_split(std::string& s, char delim) {
  std::vector<int> result;
  std::string token;
  std::istringstream tokenStream(s);
  while (std::getline(tokenStream, token, delim)) {
    result.push_back(std::stoi(token));
  }
  return result;
}

std::vector<int> processInput(int i, int j, int k, int num_reduc, std::string conf_ts_list) {
  // conf_ts_list = "2,8,4,16,8,111";
  std::string performace = conf_ts_list.substr(conf_ts_list.find_last_of(',') + 1);
  float perf = std::stof(performace);
  std::string ts_list = conf_ts_list.substr(0, conf_ts_list.find_last_of(','));
  std::vector<int> ts = string_split(ts_list, ',');

  // std::cout << "Performance: " << perf << std::endl;
  // std::cout << "TS: ";
  // for (auto ii : ts) {
  //   std::cout << ii << " ";
  // }
  // std::cout << std::endl;

  SplitFactorizationMemo sfm;
  std::vector<int> pz = {i, j, k};
  std::vector<int> index_map;

  for (int i = 0; i < ts.size() - num_reduc; i += 2) {
    auto factor_list = sfm.GetFactors(pz[i / 2]);
    // std::cout << "Parr Factors for " << pz[i / 2] << " : ";
    // for (auto jj : factor_list) {
    //   std::cout << jj << " ";
    // }
    // std::cout << std::endl;

    int tb_index = std::find(factor_list.begin(), factor_list.end(), ts[i]) - factor_list.begin();
    int reg = std::find(factor_list.begin(), factor_list.end(), ts[i + 1]) - factor_list.begin();
    index_map.push_back(tb_index);
    index_map.push_back(reg);
  }

  for (int i = 0; i + (ts.size() - num_reduc) < ts.size(); i++) {
    auto factor_list = sfm.GetFactors(pz[i + (ts.size() - num_reduc) / 2]);
    // std::cout << "Reduc Factors for "
    //           << " " << pz[i + (ts.size() - num_reduc) / 2] << " : ";
    // for (auto jj : factor_list) {
    //   std::cout << jj << " ";
    // }
    // std::cout << std::endl;
    int tb_index =
        std::find(factor_list.begin(), factor_list.end(), ts[i + (ts.size() - num_reduc)]) -
        factor_list.begin();
    index_map.push_back(tb_index);
  }

  // TODO: Write to a file in CSV
  return index_map;
}


int main(int argc, char** argv) {
  // User input i, j, k, num_reduc
  int i = argv[1] ? std::stoi(argv[1]) : -1;
  int j = argv[2] ? std::stoi(argv[2]) : -1;
  int k = argv[3] ? std::stoi(argv[3]) : -1;
  int num_reduc = argv[4] ? std::stoi(argv[4]) : -1;
  int testcase = argv[5] ? std::stoi(argv[5]) : -1;
  int num_start_points = argv[6] ? std::stoi(argv[6]) : -1;

  if (argc < 6) {
    std::cout << "Missing inputs" << std::endl;
    return 1;
  }

  if (i == -1 || j == -1 || k == -1 || num_reduc == -1 || testcase == -1) {
    std::cout << "Invalid input" << std::endl;
    return 1;
  }
  std::cout << "i: " << i << " j: " << j << " k: " << k << std::endl;
  std::cout << "Num reduc: " << num_reduc << std::endl;
  std::cout << "Testcase: " << testcase << std::endl;

  std::vector<int> pz = {i, j, k};

  SplitFactorizationMemo sfm;

  double exe_time;
  int age;
  for (int ite = 0; ite < num_start_points; ite++) {
    std::string input_csv = "data/_output/" + std::to_string(ite) +
                            "cuda_testCase_" + std::to_string(testcase) +
                            "_matmul_M" + std::to_string(i) +
                            "_N" + std::to_string(j) +
                            "_K" + std::to_string(k) + ".csv";

    std::cout << "Input CSV: " << input_csv << std::endl;

    std::ifstream file(input_csv);
    std::string conf_ts_list;
    if (file.is_open()) {
      std::string line;
      while (std::getline(file, line)) {
        if (line.find("tile_sizes") != std::string::npos) {
          continue;
        }
        // std::cout << "Line: " << line << std::endl;
        exe_time = std::stod(line.substr(line.find_first_of(',') + 1));
        // std::cout << "Execution time: " << exe_time << std::endl;
        
        // find the last of ',' then get age after it
        age = std::stoi(line.substr(line.find_last_of(',') + 1));
        // std::cout << "Age: " << age << std::endl;

        // find two " , get the string between them
        conf_ts_list = line.substr(line.find_first_of('"') + 1,
                                   line.find_last_of('"') - line.find_first_of('"') - 1);
        // std::cout << "Conf TS list: " << conf_ts_list << std::endl;

        conf_ts_list += "," + std::to_string(exe_time);
        // std::cout << "Final Conf TS list: " << conf_ts_list << std::endl;

        std::vector<int> index_map = processInput(i, j, k, num_reduc, conf_ts_list);

        // std::cout << "Index map size: " << index_map.size() << std::endl;
        // for (auto ii : index_map) {
        //   std::cout << ii << " ";
        // }
        // std::cout << std::endl;

        // Connect to CSV output
        std::string output_csv = input_csv.substr(0, input_csv.find_last_of('.')) + "_index.csv";
        std::ofstream output_file(output_csv, std::ios::app);
        if (output_file.is_open()) {
          for (auto ii : index_map) {
            output_file << ii << ",";
          }
          output_file << exe_time << ",";
          output_file << age << std::endl;
          output_file.close();
        } else {
          exit(-1);
        }
      }
      file.close();
    } else {
      std::cout << "Unable to open file" << std::endl;
      exit(-1);
    }
  }

  return 0;
}
