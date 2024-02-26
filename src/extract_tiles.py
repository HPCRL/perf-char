import ast
import json
import os
import pandas as pd

# dsc: get value from json line
# line: json line
# key: key of the value
def get_from_json_line(line, key):
    try:
        data = json.loads(line)
        value = data.get(key, None)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in line: {line}")
        value = None
    return value

def convert_tile_sizes(raw_data):
    sp_entries = [
        entry for entry in raw_data[1][1] if entry[0] == "SP"
    ]

    # i/j/k map
    map_dim = {}
    tile_sizes = []
    for ite, entry in enumerate(sp_entries):
        if entry[0] == "SP":
            tile_sizes.append(entry[4])
            map_dim[ite] = entry[4]
        if ite == 3:
            break

    # print(tile_sizes)
    # print(map_dim)
    combined_tile_sizes = []
    for sizes in tile_sizes:
        combined_tile_sizes.extend(sizes)

    # print(combined_tile_sizes)

    # Convert tile sizes to desired format
    tb1 = tile_sizes[0][1]
    reg1 = tile_sizes[0][0] * tile_sizes[0][2] * tile_sizes[0][3]
    tb2 = tile_sizes[1][1]
    reg2 = tile_sizes[1][0] * tile_sizes[1][2] * tile_sizes[1][3]
    sm3 = tile_sizes[2][0] * tile_sizes[2][1]

    tile_sizes = f'"{tb1},{reg1},{tb2},{reg2},{sm3}"'

    # print(tile_sizes)
    # input("Press Enter to continue...")

    return tile_sizes


def process_file(file_path):
    tile_sizes_list = []
    exe_time_list = []
    ag_list = []
    marker_list = []
    with open(file_path, 'r') as file:
        for line in file:
            raw_data = get_from_json_line(line, "i")
            exe_time = get_from_json_line(line, "r")[0][0]
            age = get_from_json_line(line, "ag")
            marker = get_from_json_line(line, "mark")
            # print(exe_time)
            tile_sizes = convert_tile_sizes(raw_data)
            tile_sizes_list.append(tile_sizes)
            exe_time_list.append(exe_time)
            ag_list.append(age)
            marker_list.append(marker)

    tile_sizes_list = [s.replace('"', '') for s in tile_sizes_list]
    # Create _output folder if it doesn't exist
    output_folder = "data/_output"
    os.makedirs(output_folder, exist_ok=True)
    
    # Write to CSV file
    file_name = os.path.basename(file_path)
    csv_file_path = os.path.join(output_folder, file_name.replace(".json", ".csv"))
    
    df = pd.DataFrame({'index': range(len(tile_sizes_list)), 'exe_time': exe_time_list, 'tile_sizes': tile_sizes_list, 'mark': marker_list, 'age': ag_list})
    df.to_csv(csv_file_path, index=False, header=['index', 'exe_time', 'tile_sizes', 'mark', 'age'])
    
    return tile_sizes_list, exe_time_list

def main(folder_path):
    json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]
    
    for json_file in json_files:
        print(f"Processing file: {json_file}")
        file_path = os.path.join(folder_path, json_file)
        tile_sizes_list, exe_time_list = process_file(file_path)
        # print(tile_sizes_list)
        # print(exe_time_list)
        
        assert len(exe_time_list) == len(tile_sizes_list)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extract_tiles.py <folder_path>")
        exit(1)
        
    folder_path = sys.argv[1]
    main(folder_path)
