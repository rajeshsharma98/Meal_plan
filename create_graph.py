import pandas as pd
import json

def create_graph(input_file, output_file):
    df = pd.read_csv(input_file)

    data_top = df.columns
    # print(data_top[2:])

    adj_list = {}

    for row in df.itertuples():
        for col in data_top[2:]:
            pair = [col, float(getattr(row, col))]
            if row.name not in adj_list.keys():
                adj_list[row.name] = []
            adj_list[row.name].append(pair)

            pair2 = [row.name, float(getattr(row, col))]
            if col not in adj_list.keys():
                adj_list[col] = []
            adj_list[col].append(pair2)

    # print(adj_list)
    json_data = json.dumps(adj_list)

    # open file for writing, "w" 
    f = open(output_file,"w")

    # write json object to file
    f.write(json_data)

    # close file
    f.close()

# example usage 
create_graph("./dataset/STANDARD_VALUES.csv", "./dataset/adj_list.json")