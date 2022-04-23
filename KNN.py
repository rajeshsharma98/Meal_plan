import pickle
import numpy as np
import json
import argparse

''' Function to calculate distance'''
def distance(a ,b):
    x = np.array(a)
    y = np.array(b)
    return np.linalg.norm(a - b)

''' Functiont to open a pickle file'''
def open_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f) 
    return data

''' Function to get the nearest neighbors'''
def knn(input,embed_file,cluster_file,adj_list,k):  
    # open the files
    cluster_all = open_file(cluster_file) # ouput-> nested list where each list represents the clusters
    embed_all = open_file(embed_file) # output -> dictionary wherre key is the node and its values is the embedding
    adj_graph = adj_list_reader(adj_list) # output -> adjecency list in dictionary format

    # set for 2 set of node
    s = [] # fetching column names
    s1, s2 = fetch_bipartite_graph_node(adj_graph)
    if len(s1) > len(s2):
        s = s2
    else:
        s = s1

    # removing columns name nodes from embedding dataset
    embed = {key: embed_all[key] for key in embed_all if key not in s}
    # removing columns name nodes from cluster dataset also
    cluster = [[j for j in i if j not in s] for i in cluster_all]


    # # Get new point key and values
    # new_pointKey = [*input.keys()][0]
    # new_point = [*input.values()][0]
    
    # Input point and its embedding
    new_pointKey = input
    new_point = embed[input]

    # check which cluster item belong -> only retain all the values of that cluster
    # check if point in which cluster
    if (new_pointKey in x for x in cluster): # if point in the cluster nested lists
        for i in range(len(cluster)): # fetch the index of the cluster item belongs
            if new_pointKey in cluster[i]:
                cluster_index = i
        
        # only retain embeddings of the cluster input item belongs
        embed = {key: embed[key] for key in cluster[cluster_index]}
        # remove the input from the embedding dictionary
        del embed[input]

        keys = [*embed.keys()] # all keys
        data = [*embed.values()] # all key values
        # calculate distance of the point to every other item(cluster item)
        distance = np.linalg.norm(np.array(data) - np.array(new_point), axis=1)
        # sort indexes of the cluster according to the distance
        nearest_neighbor_ids = distance.argsort()[:k]
        # fetch ingredient names of nearest neighbor
        result = ([keys[i] for i in nearest_neighbor_ids])
        print(result)
    else:
        print("Item not in the dataset")

def remove(nested_list,filter):
    for i in nested_list:
        for j in filter:
            if j in i:
                
                i.pop(i.index(j))


''' function to color nodes in bipartite graph '''
def fetch_bipartite_graph_node(adj_list):
    colors = {}
    for key in adj_list.keys():
        colors[key] = 0
    
    for key in colors.keys():
        if colors[key] == 0 and (not dfs(adj_list, colors, 1, key)):
            raise Exception("not bipartite");

    s1 = []
    s2 = []
    for key in colors.keys():
        if colors[key] == 1:
            s1.append(key)
        else:
            s2.append(key)

    return s1, s2;

''' helper function '''
def dfs(adj, color, current_color, node):
    if color[node] != 0:
        return current_color == color[node]
    else:
        color[node] = current_color
        neighbours = adj[node]
        for neighbour in neighbours:
            if (not dfs(adj, color, -1 * current_color, neighbour[0])):
                return False
    return True

''' util to read adjacency list'''
def adj_list_reader(file):
    adj_list = {};
    # Opening JSON file
    with open(file) as json_file:
        adj_list = json.load(json_file)
    return adj_list

'''Usage'''

# input from user
parser = argparse.ArgumentParser()
parser.add_argument('-q', '--input_query', help='specify the query node')
parser.add_argument('-e', '--embed_file', help='specify the embedding file')
parser.add_argument('-c', '--cluster_file', help='specify the cluster file')
parser.add_argument('-adj', '--adj_list_file', help='specify the adjancency list file')
parser.add_argument('-k', '--neighbours', help='specify the number of neighbours')

args = parser.parse_args()

input = args.input_query # Input is the name of the ingredient
embed_file = args.embed_file  # embedding file -> dictionary wherre key is the node and its values is the embedding
cluster_file = args.cluster_file # cluster file -> nested list where each list represents the clusters
adj_list = args.adj_list_file # adjacency list
k = int(args.neighbours) # number of nearest neighbors to fetch

# invoke helper fuction
knn(input, embed_file, cluster_file, adj_list, k)

## example usage
## time python KNN.py -q Cornstarch -e deep_walk_8_baised_walk_3_4.pickle -c cluster_10_20_deep_walk_8_baised_walk_3_4.pickle -adj -k 15