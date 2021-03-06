import math
from random import randint

import numpy as np
import pandas as pd
from sklearn import datasets

import matplotlib.pyplot as plt

# ***************************************************************
# Function:         run_kbrain
# Variables/input:  int: k number of clusters to find
#                   string: algorithm to perform
#                   objects.dataset: dataset to work on
# Output:           pandas dataframe: cluster assignments
# Usage/Purpose:    Function calls k-means or k-medoid and
#                   returns the cluster assignment for each
#                   datapoint.
# ***************************************************************
def run_kbrain(k, algorithm, data):

    return_df = pd.DataFrame()

    # if data == None:
    #    data = generate_random_dataset()

    initial_centers = generate_random_centers(k, data.df)

    label, centers = generate_clusters(k, data, initial_centers, algorithm)

    # autoplot(k, data.df, centers, label, algorithm)

    return_df["clusters"] = label

    return pd.DataFrame(label, columns=["cluster"])


# ***************************************************************
# Function:         autoplot
# Variables/input:  int: k number of clusters to find
#                   pandas dataframe: data to plot
#                   float: coordinates of cluster centers
#                   labels
# Output:           generates plot of data clusterings
# Usage/Purpose:    Function generates plots of data clusterings
# ***************************************************************
def autoplot(k, df, centers, labels, alg):
    # NOTE: Only works for two dimensions currently
    for n in range(0, k):
        plt.scatter(df.x1[labels == n], df.x2[labels == n])
        plt.scatter(centers[n][0], centers[n][1], c="k")

    title = alg + " with K = " + str(k)
    plt.title(title)
    plt.show()
    plt.clf()


# ***************************************************************
# Function:         euclidean_distance
# Variables/input:  list[float]: x, y coordinates of point 1
#                   list[float]: x, y coordinates of point 2
# Output:           float: distance between points
# Usage/Purpose:    Function calculates the euclidean distance
#                   between two points.
# ***************************************************************
def euclidean_distance(pointA, pointB):
    # Function returns the euclidean distance between two points
    return_dist = 0

    # Dynamically calculate the euclidean distance for all dimensions
    for n in range(0, len(pointA)):
        return_dist += (pointA[n] - pointB[n]) ** 2

    # Return the distance
    return math.sqrt(return_dist)


# ***************************************************************
# Function:         kmean
# Variables/input:  int: k number of clusters to find
#                   list[float]: cluster points
#                   labels
# Output:           list[float]: centroids
# Usage/Purpose:    Function calculates centroids.
# ***************************************************************
def kmean(k, clusters, labels):
    # Function returns new centroids based on the means of the clusters
    return_centroids = []

    # For cluster n of k...
    for n in range(0, k):

        # Calculate the mean
        temp = np.mean(clusters.df[labels == n])

        # Append the new centroid to the return array
        return_centroids.append(temp.values)

    # Return the new centroids
    return return_centroids


# ***************************************************************
# Function:         kmedoid
# Variables/input:  int: k number of clusters to find
#                   list[float]: cluster points
#                   medoids
#                   labels
# Output:           list[float]: centroids
# Usage/Purpose:    Function calculates centroids.
# ***************************************************************
def kmedoid(k, clusters, medoids, labels):
    # Function returns new medoids by calculating which point of the cluster
    # has the lowest entropy
    return_medoids = []

    # Generate arrays for data
    init = np.empty(k)
    distances = np.ones(k) * np.inf

    # For cluster n of k...
    for n in range(0, k):
        length = len(clusters.df[labels == n])

        # Iterate through every point of each cluster
        i = length - 1

        # Save the cluster once, use it a lot
        cluster = clusters.df[labels == n]
        while i >= 0:
            temp = 0

            # For point m in cluster n
            for m in range(0, length):

                # Calculate the total distance from all points to the
                # prospective medoid
                temp += clusters.distanceArray[cluster.index[m], cluster.index[i]]

            # If the prospective medoid has lower entropy than the current
            if temp < distances[n]:

                # Replace the old medoid with the new medoid and save the distance
                distances[n] = temp
                init[n] = i

            i -= 1

        # Append the new medoid to the return array
        return_medoids.append(cluster.iloc[int(init[n])].values)

    # Return the new medoids
    return return_medoids


# ***************************************************************
# Function:         generate_random_dataset
# Variables/input:  none
# Output:           pandas dataframe: dataset points
# Usage/Purpose:    Function generates a random dataset.
# ***************************************************************
def generate_random_dataset():
    # Function returns a dataframe with X/Y pairs and a column for cluster labels
    return_df = pd.DataFrame(columns=["x1", "x2"])

    # Generate a blob set to my liking for now
    X, y = datasets.make_blobs(n_samples=50, n_features=4, center_box=(-3.0, 3.0))

    # Convert the blobs into two arrays aka X and Y coords
    A = np.append(X[:, 0], X[:, 2])
    B = np.append(X[:, 1], X[:, 3])

    # Save the X and Y coords in the return Dataframe
    return_df.x1 = A
    return_df.x2 = B

    # Return the dataset
    return return_df


# ***************************************************************
# Function:         generate_random_centers
# Variables/input:  int: k number of clusters to find
#                   pandas dataframe: dataset
# Output:           list[float]: centers of clusters
# Usage/Purpose:    Function generates a random center.
# ***************************************************************
def generate_random_centers(k, df):
    # Function returns random centers to begin clustering
    return_centers = []
    init = []

    # Save the number of points once, use it k times
    numPoints = len(df) - 1

    # For each center generation n...
    for n in range(0, k):

        # Roll for an index from the data
        rnd = randint(0, numPoints)

        # If the index has already been chosen, reroll
        while rnd in init:
            rnd = randint(0, numPoints)

        # Append the new index to the init array
        init.append(rnd)

        # Append the new center to the return array
        return_centers.append(df.iloc[init[n]].values)

    # Return the centers
    return return_centers


# ***************************************************************
# Function:         generate_clusters
# Variables/input:  int: k number of clusters to find
#                   list[float]: points
#                   list[float]: centers
#                   string: algorithm name
# Output:           pandas dataframe: cluster assignments
#                   cluster centers
# Usage/Purpose:    Function generates clusters according to
#                   k-means or k-medoid algorithm.
# ***************************************************************
def generate_clusters(k, points, centers, algorithm):
    # Function returns a list of cluster labels
    length = len(points.df)
    return_labels = np.empty(length)

    # Base cases
    if k == 0:
        print("I don't know what you expected...")

    elif k == 1:
        return_labels = np.zeros(length)

    elif k == length:
        return_labels = np.arange(0, length)

    # The meat of it
    else:
        while 1:

            # For point n...
            for n in range(0, length):

                # Reset the current distance
                currentDist = np.inf

                # For cluster m...
                for m in range(0, k):

                    # Calculate the euclidean distance between point n
                    # and center m
                    newDist = euclidean_distance(points.df.iloc[n], centers[m])

                    # If the new distance is less than the current distance...
                    if newDist < currentDist:

                        # Save the new distance
                        currentDist = newDist

                        # Set the cluster label as m for point n
                        return_labels[n] = m

            # Algorithm pseudo-switch statement
            if algorithm == "k-means":
                new_centers = kmean(k, points, return_labels)

            elif algorithm == "k-medoids":
                new_centers = kmedoid(k, points, centers, return_labels)

            else:
                print("Error: invalid algorithm")
                return None

            # Check if the new centers are the same as the old centers
            if np.array_equal(new_centers, centers):
                # If so, break
                break
            else:
                centers = new_centers

    # Return the cluster labels and the final centers
    return return_labels, centers
