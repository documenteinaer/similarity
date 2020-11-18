#!/bin/python

from utils import *

locations = []

# AP positions
def plot_similarities(location):
    physical_plot = []
    cosine_plot = []
    cityblock_plot = []
    euclidean_plot = []
    minkowski_plot = []
    jaccard_plot = []

    # Plot only for nearest locations
    for l in get_nearest_locations(location, locations, 10):

        # Skip the exact location
        if physical_distance(l, location) == 0:
            continue

        # Create the similarity arrays
        physical_plot.append(physical_distance(l, location))
        cosine_plot.append(cosine(tuple(l[3]), tuple(location[3])))
        cityblock_plot.append(cityblock(tuple(l[3]), tuple(location[3])))
        euclidean_plot.append(euclidean(tuple(l[3]), tuple(location[3])))
        minkowski_plot.append(minkowski(tuple(l[3]), tuple(location[3]), 3))
        jaccard_plot.append(jaccard(tuple(l[3]), tuple(location[3])))

    # Plot similarities. Due to scalling issues, it's better to select only one
    #plt.plot(physical_plot, cityblock_plot, 'o', label = "line 1")
    #plt.plot(physical_plot, euclidean_plot, 'o', label = "line 1")
    #plt.plot(physical_plot, minkowski_plot, 'o', label = "line 1")
    #plt.plot(physical_plot, cosine_plot, 'o', label = "line 1")
    plt.plot(physical_plot, jaccard_plot, 'o', label = "line 1")

    # Standardization: scale the similarity from -4 to +4
    #plt.plot(physical_plot, preprocessing.scale(cityblock_plot), 'o', label = "line 1")
    #plt.plot(physical_plot, preprocessing.scale(euclidean_plot), 'o', label = "line 2")
    #plt.plot(physical_plot, preprocessing.scale(minkowski_plot), 'o', label = "line 3")
    #plt.plot(physical_plot, preprocessing.scale(cosine_plot), 'o', label = "line 4")
    #plt.plot(physical_plot, preprocessing.scale(jaccard_plot), 'o', label = "line 5")

    plt.legend()
    plt.show()

def plot_common_APs(location):
    common_APs = []
    APs_only_1 = []
    APs_only_2 = []
    physical_distances = []

    for l in locations:
        # Skip the exact location
        if physical_distance(l, location) == 0:
            continue
        APs_only_1.append(get_common_APs(location, l)[0])
        APs_only_2.append(get_common_APs(location, l)[1])
        common_APs.append(get_common_APs(location, l)[2])
        physical_distances.append(physical_distance(location, l))

    print(common_APs)
    plt.plot(physical_distances, common_APs, 'o', label = "Number of APs")
    #plt.plot(physical_distances, APs_only_1, 'o', label = "APs only in current location")
    #plt.plot(physical_distances, APs_only_2, 'o', label = "APs not in current location")
    plt.legend()
    plt.show()


loc1 = int(sys.argv[1])

locations = load_dataset()
norm_rss(locations)

plot_common_APs(locations[loc1])

#plot_similarities(locations[loc1])
