#!/bin/bash

echo "## Running graph project.... ##"

# echo "## deleting directories ##"
rm -rf dataset/
rm -rf embeddings/
rm -rf clusters/
rm -rf visualization/

echo "## creating dataset directory ##"
mkdir dataset

echo "## creating embeddings directory ##"
mkdir embeddings

echo "## creating clusters directory ##"
mkdir clusters

echo "## creating visualization directory ##"
mkdir visualization

echo "## installing dependencies ##"
pip3 install -r requirements.txt

echo "## creating standard data ##"
## TODO: review standardise code
python3 standardize.py

echo "## creating adjacency list of graph  ##"
python3 create_graph.py

# embedding variables
# walk-length - 30, 90, 256
# number-of-walks - 32
# dimensions - 16, 64, 128

# clusering variables
# clusters - 10, 74
# iteration - 100

# visualisation
# axis - 2D,3D

# carbonate
wl=(30 90 128)
nw=32
dim=(16 64 128)
cluster=(10 74)
iteration=100
ax=(2 3)

# local
# wl=(2)
# nw=1
# dim=(2)
# cluster=(2)
# iteration=20
# ax=(2 3)

# running embedding
echo "## generating embeddings  ##"
cd embeddings
for walk_len in ${wl[@]}
do
    for dimension in ${dim[@]}
        do 
            echo "####---- running embedding: walk length-$walk_len, number of walks-$nw, dimension-$dimension ----####"
            python3 -m gembed.embed deep_walk -w $nw -wl $walk_len -d $dimension -walker baised_walk -adj_list ../dataset/adj_list.json
        done
done
cd ..

# running clustering
echo "## running clustering ##"
for c in ${cluster[@]}
do
    for walk_len in ${wl[@]}
    do
        for dimension in ${dim[@]}
            do 
                echo "####---- running clustering on file : deep_walk_${dimension}_baised_walk_${nw}_${walk_len}.pickle, clusters-${c}, iteration-${iteration} ----####"
                python3 clustering.py -i ./embeddings/deep_walk_${dimension}_baised_walk_${nw}_${walk_len}.pickle -o ./clusters/cluster_${c}_${iteration}_deep_walk_${dimension}_baised_walk_$nw_${walk_len}.pickle -k ${c} -e ${iteration}
            done
    done
done

# visualisation of clusters in 2/3 D using TSNE technique
echo "## visualisation of clusters in 2/3 D using TSNE technique ##"
cd visualization
for axis in ${ax[@]}
do
    for c in ${cluster[@]}
    do
        for walk_len in ${wl[@]}
        do
            for dimension in ${dim[@]}
                do 
                    echo "####---- running visualisation on file : cluster_${c}_${iteration}_deep_walk_${dimension}_baised_walk_${nw}_${walk_len}.pickle, axes-${axis} ----####"
                    python3 ../visualization.py -e ../embeddings/deep_walk_${dimension}_baised_walk_${nw}_${walk_len}.pickle -c ../clusters/cluster_${c}_${iteration}_deep_walk_${dimension}_baised_walk_$nw_${walk_len}.pickle -d ${axis}
                done
        done
    done
done
cd ..

# Suggesting substitutes using KNN
# echo "## Suggesting substitutes using KNN ##"
# python3 KNN.py -q 'Alcoholic beverage, cooking, wine' -e ./embeddings/deep_walk_8_baised_walk_3_4.pickle -c  ./clusters/cluster_10_20_deep_walk_8_baised_walk_3_4.pickle -adj ./dataset/adj_list.json -k 15


echo "Done.... :)"
