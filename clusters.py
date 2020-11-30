#!/usr/bin/env python

import argparse
import sys
import settings
from objects import experiment, dataset
from dbscan import dbscan
import pandas as pd
from sklearn import datasets
import time
import math
import numpy as np
from sklearn_algs import sklearn_kmeans, sklearn_kmedoids, sklearn_dbscan


def main():
    # process command line arguments and return arguments as args
    args = run_parser()

    # load or build datasets according to arguments
    datasets = ready_datasets(args)

    # build experiment object, including datasets
    exp = experiment(datasets, settings.algorithms)

    # calculate distances for each dataset
    calculate_distances(exp)

    # run an experiment with all algorithms and datasets
    if args.experiment:
        run_experiment(exp)

    # run k-means algorithm on specified datasets
    if args.kmeans:
        # call k-means wrapper function
        print()

    if args.kmedoids:
        # call k-medoids wrapper function
        print()

    if args.dbscan:
        # call dbscan wrapper function
        print()

    # process results here
    print_results(exp)


# replace this comment with proper formater
# this function takes an experiment and runs
# all specified permutations of the parameters
def run_experiment(exp):
    # loop through each clustering algorithm
    for algo in exp.algorithms:

        # loop through each dataset
        for ds in exp.datasets:

            # loop through the number of datapoints
            # to be used
            for num in settings.numSamples:

                # loop for each trial run
                for i in range(1, settings.numRuns + 1):

                    # call dbscan with parameters
                    if algo == "DBSCAN":

                        # loop parameters unique to dbscan
                        for eps in settings.epsilons:
                            for mp in settings.minPts:

                                # call dbscan with parameters
                                results = dbscan(ds, num, eps, mp)

                                # save results of each experiment
                                exp.results[algo].append(
                                    (ds.name, num, i, eps, mp, results)
                                )

                    if algo == "k-means":

                        # call k-means and save results here
                        print()

                    if algo == "k-medoid":

                        # call k-medoid and save results here
                        print()

                    if algo == "sklearn_kmeans":
                        for numClusters in range(1, 5):
                            results = sklearn_kmeans(ds, numClusters, num)

                            exp.results[algo].append(
                                (ds.name, num, i, numClusters, results)
                            )

                    if algo == "sklearn_kmedoids":
                        for numClusters in range(1, 5):
                            results = sklearn_kmedoids(ds, numClusters, num)

                            exp.results[algo].append(
                                (ds.name, num, i, numClusters, results)
                            )

                    if algo == "sklearn_dbscan":
                        # loop parameters unique to dbscan
                        for eps in settings.epsilons:
                            for mp in settings.minPts:

                                # call dbscan with parameters
                                results = sklearn_dbscan(ds, num, eps, mp)

                                # save results of each experiment
                                exp.results[algo].append(
                                    (ds.name, num, i, eps, mp, results)
                                )


def print_results(exp):
    print("Analyse Results\n")

    for algo in exp.results.keys():
        if algo == "DBSCAN" or algo == "sklearn_dbscan":
            all_results = exp.results[algo]

            for results in all_results:
                print(
                    "Experiment:\n\tAlgorithm: {0}\n\tDataset Name: {1}\n\tNum Datapoints: {2}\n\tTrial Number: {3}\n\tEpsilon: {4}\n\tMin Points: {5}".format(
                        algo, results[0], results[1], results[2], results[3], results[4]
                    )
                )
                print("Cluster Assignments:\n")
                print(results[5])

        elif algo == "sklearn_kmeans":
            all_results = exp.results[algo]

            for results in all_results:
                print(
                    "Experiment:\n\tAlgorithm: {0}\n\tDataset Name: {1}\n\tNum Datapoints: {2}\n\tTrial Number: {3}\n\tNumber Clusters: {4}".format(
                        algo, results[0], results[1], results[2], results[3]
                    )
                )
                print("Cluster Assignments:\n")
                print(results[4])

        elif algo == "sklearn_kmedoids":
            all_results = exp.results[algo]

            for results in all_results:
                print(
                    "Experiment:\n\tAlgorithm: {0}\n\tDataset Name: {1}\n\tNum Datapoints: {2}\n\tTrial Number: {3}\n\tNumber Clusters: {4}".format(
                        algo, results[0], results[1], results[2], results[3]
                    )
                )
                print("Cluster Assignments:\n")
                print(results[4])


# add appropriate comments
# this function uses command line arguments to generate
# datasets from csv or sklearn
def ready_datasets(args):
    datasetReturn = []

    # load dataset from csv.  this has not been tested
    # the csv part could be abstracted into another function
    if args.dataset:
        dfCSV = pd.read_csv(args.dataset, columns=["x1", "x2"])
        datasetReturn.append(dataset(args.dataset, dfCSV))

        print("dataset read from {0}".format(args.dataset))
        print(dfCSV.head(5))

    # loop through all sklearn dataset types and add a new
    # dataset object to the return list
    if args.generate:
        for name in settings.datasetTypes:
            datasetReturn.append(dataset(name, build_dataset(name)))

    return datasetReturn


# add formatted comments
# function takes the name of an sklearn dataset type
# and builds a dataframe dataset of that type
def build_dataset(name):
    # build all the dataset types here
    df = pd.DataFrame()

    # generate sklearn circles dataset
    if name == "circles":
        new_dataset = datasets.make_circles(
            n_samples=settings.maxSamples, factor=0.5, noise=0.05
        )

    elif name == "moons":
        new_dataset = datasets.make_moons(n_samples=settings.maxSamples, noise=0.05)

    elif name == "blobs":
        new_dataset = datasets.make_blobs(n_samples=settings.maxSamples, random_state=1)

    # convert to dataframe
    df = pd.DataFrame(new_dataset[0], columns=["x1", "x2"])

    # add cluster labels to dataframe
    df["y"] = new_dataset[1]

    # print functions can be deleted once finished
    print("{0} dataset generated".format(name))
    print(df.head(5))

    return df


def calculate_distances(exp):
    print("calculate_distances")

    for ds in exp.datasets:
        df = ds.df

        getDistancesTimeStart = time.perf_counter()

        ds.distanceArray = np.zeros(
            [settings.maxSamples, settings.maxSamples], dtype=float
        )

        for i in range(settings.maxSamples):
            for j in range(i, settings.maxSamples):
                if i == j:
                    continue

                distance = math.sqrt(
                    math.pow(df.iloc[i]["x1"] - df.iloc[j]["x1"], 2)
                    + math.pow(df.iloc[i]["x2"] - df.iloc[j]["x2"], 2)
                )

                ds.distanceArray[i, j] = distance
                ds.distanceArray[j, i] = distance

        getDistancesTimeStop = time.perf_counter()

        print(
            "get_distances time: {0:5.4}\n".format(
                (getDistancesTimeStop - getDistancesTimeStart) * 100
            )
        )


# add formatted comments
# this function uses 'argparse' library to parse
# command line arguments
# this function will terminate program if inappropriate
# arguments are given
# more checks of arguments need to be coded
def run_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--dataset", action="store", help="path to a csv dataset {./dataset.csv}"
    )
    parser.add_argument(
        "-g", "--generate", action="store_true", help="generate all dataset types"
    )

    parser.add_argument(
        "-e", "--experiment", action="store_true", help="run all clustering algorithms"
    )

    parser.add_argument(
        "-m", "--kmeans", action="store_true", help="run only the k-means algorithm"
    )

    parser.add_argument(
        "-o", "--kmedoids", action="store_true", help="run only the k-medoids algorithm"
    )

    parser.add_argument(
        "-s", "--dbscan", action="store_true", help="run only the dbscan algorithm"
    )

    if len(sys.argv) == 1:
        print("\nPlease provide command line arguments")
        print("Choose one of the following:")
        print("-d or --dataset {./dataset.csv}")
        print("-g or --generate to generate several dataset types\n")
        print("Choose one of the following:")
        print("-e or --experiment to run all algorithms")
        print("-m or --kmeans to run only the k-means algorithm")
        print("-o or --kmedoid to run only the k-medoid algorithm")
        print("-s or --dbscan to run only the dbscan algorithm\n")
        exit()

    args = parser.parse_args()

    if args.dataset:
        print("Path to csv: {0}".format(args.dataset))

    if args.generate:
        print("The following datasets will be generated:")
        print("\tlist some datasets")

    return args


main()