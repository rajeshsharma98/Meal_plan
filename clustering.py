import pickle
import numpy as np
from multiprocessing import Pool
from functools import partial
import argparse
from tqdm import tqdm


''' function for kmeans clustering '''
def kmeans(embedding, k, max_iter, tolerence):

    data = [[] for x in range(len(embedding))]

    # preprocessing embeddings
    index = 0
    mapping = {}
    for key in embedding.keys():
        data[index] = embedding[key]
        mapping[index] = key
        index += 1

    centroids = [[] for x in range(k)] 
    clusters = [[] for x in range(k)]

    # initialize centroids
    for i in range(k):
        centroids[i] = data[i]

    # iterations
    pbar = tqdm(total = max_iter)
    while (max_iter > 0):

        # distance from each centroid
        dist = [[] for x in range(k)]

        for i in range(k):
            dist[i] = distance_centroid(data, centroids[i]);

        # with Pool(processes=4) as pool: #create a pool object to use multiprocessing for faster computation
        #     dist = pool.map(partial(distance_centroid, data) ,centroids)
        # pool.close()
        # pool.join()

        # clear clusters
        for i in range(k):
            clusters[i] = [] 

        # min distance from each point to centroids
        dim = len(dist[0])
        for col in range(dim):
            min_index = dim
            min_value = float('inf')
            for row in range(len(dist)):
                if min_value > dist[row][col]:
                    min_value = dist[row][col]
                    min_index = row
            # assign to cluster
            clusters[min_index].append(col) 

        # update centroids
        for i in range(k):
            centroids[i] = avg_points(data, clusters[i])

        max_iter -= 1

        # update progress bar        
        pbar.update(1)


    # final result
    result = []

    for cluster in clusters:
        temp = []
        for item in cluster:
            temp.append(mapping[item])
        result.append(temp)

    return result

'''
function to calculate distance of all data points from centroid
'''
def distance_centroid(data, centroid):
    dist = []
    for row in data:
        dist.append(distance(row, centroid))
    return dist

'''
function to caluculate distance between two points
'''
def distance(a ,b):
    x = np.array(a)
    y = np.array(b)
    return np.linalg.norm(a - b)

'''
function to calculate new centroid
'''
def avg_points(data, index_list):
    dim = len(data[0])
    avg = [0] * dim

    if len(index_list) == 0:
        return avg

    for index in index_list:
        avg += data[index]
    avg /= len(index_list)
    return avg

'''
Helper functions for invoking kmeans
'''
def clustering(input, output, k, max_iter):   
    # read embedding
    with open(input, 'rb') as handle:
        embedding = pickle.load(handle)

        # clustering
        result = kmeans(embedding, k, max_iter, 0.001);
        
        # writing results
        with open(output, 'wb') as outhandle:
            pickle.dump(result, outhandle, protocol=pickle.HIGHEST_PROTOCOL)


# input from user
parser = argparse.ArgumentParser();

parser.add_argument('-ip', '--input_file', help='specify the input file');
parser.add_argument('-op', '--output_file', help='specify the output file');
parser.add_argument('-k', '--clusters', help='specify the cluster size');
parser.add_argument('-e', '--max_iter', help='specify the max interations');

args = parser.parse_args();

ip = args.input_file
output = args.output_file
cluster = int(args.clusters)
max_iter = int(args.max_iter)

# invoke helper fuction
clustering(ip, output, cluster, max_iter)

## example usage
## time python clustering.py -i deep_walk_baised_walk_50_15.pickle -o result_deep_walk_baised_walk_50_15 -k 10 -e 100