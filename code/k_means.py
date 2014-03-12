# Emilie de Longueau
# HMK 6 - K-means in 1 dimension

import random
import numpy
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

# Implement simple k-means clustering using 1 dimensional data


dataset = [-13.65089255716321, -0.5409562932238607, -88.4726466247223, 39.30158828358612, 4.066458182574449, 64.64143300482378, 38.68269424751338, 33.42013676314311, 31.18603331719732, -0.2027616409406292, 45.13590038987272, 30.791899783552395, 61.1727490302448, 18.167220741624856, 88.88077709786394, -1.3808002119514704, 50.14991362212521, 55.92029956281276, -6.759813255299466, 34.28290084421072]
k = 2 # number of clusters



""" Helper functions"""

def pick_centroids(xs, num):
    #Return list of num centroids given a list of numbers in xs
    k_list = random.sample(xs,num) # values picked randomly from xs list
    return k_list

def distance(a, b):
    #Return the distance of numbers a and b"""
    return abs(b-a)


def centroid(xs):
    #Return the centroid number given a list of numbers, xs
    return numpy.mean(xs)

def cluster(xs, centroids):
    #Return a list of clusters centered around the given centroids.  Clusters are lists of numbers.

    clusters = [[] for c in centroids]

    for x in xs:
        # find the closest cluster to x
        dist, cluster_id = min((distance(x, c), cluster_id)
                for cluster_id, c in enumerate(centroids))
        # place x in cluster
        clusters[cluster_id].append(x)
    return clusters


def iterate_centroids(xs, centroids):
    #Return stable centroids given a dataset and initial centroids (and also last observed error)

    err = 0.001  # minimum amount of allowed centroid movement
    observed_error = 1  # Initialize: maxiumum amount of centroid movement
    new_clusters = [[] for c in centroids]  # Initialize: clusters
    while observed_error > err:
        new_clusters = cluster(xs, centroids)
        new_centroids = map(centroid, new_clusters)
        observed_error = max(abs(new - old) for new, old in zip(new_centroids, centroids))
        centroids = new_centroids
    print "Final error is {0}".format(observed_error)
    return (centroids, new_clusters, observed_error) # also returns final error




"""Main part of program:"""
# Pick initial centroids
# Iterative to find final centroids
# Print results
if __name__ == '__main__':

    initial_centroids = pick_centroids(dataset, k) # initialize k centroid randomly picked
    final_centroids, final_clusters, final_error = iterate_centroids(dataset, initial_centroids)

    colors = "brcmykw" # list of colors to attribute to different clusters
    color_index = 0

    for centroid, cluster in zip(final_centroids, final_clusters):
        print "Centroid: %s" % centroid
        print "Cluster contents: %r" % cluster
        plt.scatter(cluster,[0]*len(cluster),s=10, color = colors[color_index]) # plot cluster 
        plt.scatter(centroid, 0, s=100, color = colors[color_index], marker='x') # plot centroid of the cluster
        color_index += 1

    plt.axis([-120,120,-1,1])
    plt.xlabel('data')
    plt.text(-50,0.8, 'K-mean clustering in 1-D / k=2 clusters', style='normal')
    plt.text(-20,0.7, 'Final error is {0}'.format(final_error), color='green', style='italic')
    plt.show()
    #plt.savefig('plot 1D K-mean k=2.png') # Save plot in a file instead of displaying it


