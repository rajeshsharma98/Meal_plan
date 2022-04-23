import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from tqdm import tqdm
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

'''Function to read pickle file'''
def open_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f) 
    return data

def tsne(data,cluster_number,dim,cluster_file):
    # TSNE               

    if dim==2:
        tsne = TSNE(n_components=2, verbose=1)
        z = tsne.fit_transform(data.iloc[:,:-1]) 
        # storing t-sne information into dataframe
        df = pd.DataFrame()
        df["tsne-1"] = z[:,0]
        df["tsne-2"] = z[:,1]
        # adding labels to dataframe
        df['color'] = data.color.tolist()
        
        ''' Plot'''
        # Color sequences
        palette = sns.color_palette("bright", cluster_number)
        sns.set(rc={'figure.figsize':(8,8)})
        sns.scatterplot(x='tsne-1', y='tsne-2',palette=palette, hue="color", data=df, s=30)
        plt.xlabel('TSNE-1')
        plt.ylabel('TSNE-2')
        plt.legend()
        plt.title('tsne for cluster '+str(cluster_number))
        plt.savefig(str(cluster_file[12:-7])+'_'+str(cluster_number)+"_"+str(dim)+'D'+'.png')
        # plt.show()

    elif dim==3:
        tsne = TSNE(n_components=3, verbose=1)

        z = tsne.fit_transform(data.iloc[:,:-1]) 
        # storing t-sne information into dataframe
        df = pd.DataFrame()
        df["tsne-1"] = z[:,0]
        df["tsne-2"] = z[:,1]
        df["tsne-3"] = z[:,2]
        sns.set(style = "darkgrid")
        # adding labels to dataframe
        df['color'] = data.color.tolist()
        # Color sequences
        fig = plt.figure(figsize=(8,8))
        ax = Axes3D(fig, auto_add_to_figure=False)
        fig.add_axes(ax)
        
        ''' Plot'''
        cmap = ListedColormap(sns.color_palette("bright", cluster_number).as_hex())
        sc = ax.scatter(df["tsne-1"], df["tsne-2"], df["tsne-3"], s=30,c=df['color'], marker='o', cmap=cmap, alpha=1)
        ax.set_xlabel('TSNE-1')
        ax.set_ylabel('TSNE-2')
        ax.set_zlabel('TSNE-3')
        plt.title('tsne for cluster '+str(cluster_number))
        plt.savefig(str(cluster_file[12:-7])+'_'+str(cluster_number)+"_"+str(dim)+'D'+'.png')
        # plt.show()

    else:
        print("Dimension defined not feasible to plot")



''' Function to visualzie clusters and to save that plot'''
def visualize(embed_file,cluster_file,dim=2):
    print('Visualization ...')
    #Open clustering and embedding file 
    cluster = open_file(cluster_file)
    embed = open_file(embed_file)
    clusters = len(cluster) # number of clusters 
    
    # read embedding file in dataframe for manipulation
    df1 = pd.DataFrame.from_dict(embed)
    df1 = df1.T

    # creating dictionary using clusters list where
    # key - label of the cluster
    # values - all the ingredients that belong that cluster label
    cluster_dict = {a:cluster[a] for a in range(0, len(cluster), 1)}

    # create empty column- color 
    df1['color'] = ''

    # Adding cluster labels to dataset in last 'color' column
    for j in tqdm(range(df1.shape[0])): # for every row of df1(embed) dataframe
        for i in range(len(cluster_dict)): # for every cluster list
            if (df1.index[j] in cluster_dict[i]): # if item in that cluster, save index of that cluster as cluster label
                    df1.iloc[j,-1] = i
    
    ''' Visualization after reducing the dimensions'''
    tsne(df1,clusters,dim,cluster_file)

'''Usage'''

# input from user
parser = argparse.ArgumentParser();

parser.add_argument('-e', '--embed_file', help='specify the embedding file');
parser.add_argument('-c', '--cluster_file', help='specify the cluster file');
parser.add_argument('-d', '--dim', default=2, help='specify the dimension to visualise');

args = parser.parse_args();

embed_file = args.embed_file # embedding file -> dictionary wherre key is the node and its values is the embedding
cluster_file = args.cluster_file # cluster file -> nested list where each list represents the clusters
dim = int(args.dim)

# invoke helper fuction
# dim  - dimension for the plot (2D or 3D)
visualize(embed_file, cluster_file, dim)

## example usage
## time python visualization.py -e embed.pickle -c cluster.pickle -d 3