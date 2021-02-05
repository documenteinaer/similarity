#!/bin/python

from utils import *

locations = []

"""
    This function selects the locations of interest considering:
        * physical distance
        * type of device
        * floor
        * experiment date (month)
    Next, *get_common_APs* selects only the common APs:
        * APs_in_1 and APs_in_2 are the values of the common APs

    You can plot 1 or more similarity methods by commenting lines 54-59.
"""
def plot_similarities(location):
    physical_plot = []
    cosine_plot = []
    cityblock_plot = []
    euclidean_plot = []
    minkowski_plot = []
    jaccard_plot = []
    sorensen_plot = []
    error_plot = []
    #TODO loc[3]
    APs_threshold = len(location[3])*0.1

    # Plot only for nearest locations
    for l in select_locations(location, locations, 20, same_device = True, \
                                                       same_floor = True, \
                                                       same_month = True):

        # Select only the APs that are common for both locations
        [APs_in_1, APs_in_2] = get_common_APs(l, location)

#         if len(APs_in_1) < APs_threshold
#             continue

        if not APs_in_1:
            continue
        # Create the similarity arrays
        physical_plot.append(physical_distance(l, location))
        cosine_plot.append(cosine(tuple(APs_in_1), tuple(APs_in_2)))
        cityblock_plot.append(cityblock(tuple(APs_in_1), tuple(APs_in_2)))
        euclidean_plot.append(euclidean(tuple(APs_in_1), tuple(APs_in_2)))
        minkowski_plot.append(minkowski(tuple(APs_in_1), tuple(APs_in_2)))
        jaccard_plot.append(jaccard(tuple(APs_in_1), tuple(APs_in_2)))
        sorensen_plot.append(braycurtis(tuple(APs_in_1), tuple(APs_in_2)))

    # Plot similarities. Due to scalling issues, it's better to select only one
    # Select the similarity methods to be plotted
    plt.plot(physical_plot, cityblock_plot, 'o', label = "City Block")
    plt.plot(physical_plot, euclidean_plot, 'o', label = "Euclidean")
    plt.plot(physical_plot, minkowski_plot, 'o', label = "Minkowski")
    plt.plot(physical_plot, cosine_plot, 'o', label = "Cosine")
    plt.plot(physical_plot, jaccard_plot, 'o', label = "Jaccard")
    plt.plot(physical_plot, sorensen_plot, 'o', label = "Sorensen")

    # Plot
    plt.xlim([0, 20])
    plt.ylim([0,0.2])
    plt.xlabel("Physical distance between provided location and all others (meters)")
    plt.ylabel("Disimilarity Measurement")

    plt.legend()
    plt.show()


def plot_common_APs(location):
    common_APs = []
    APs_only_1 = []
    APs_only_2 = []
    physical_distances = []
    common_zero = []
    APs_threshold = len(location[3])*0.05

    experiment_locations = select_locations(location, locations, meters = 20,
                                            same_device = False,
                                            same_floor = False,
                                            same_month = False)

    for l in experiment_locations:

        # Skip locations
        [APs_in_1, APs_in_2, APs_in_b] = get_number_APs(location, l)
        #print([APs_in_1, APs_in_2, APs_in_b])
        #if APs_in_1 < APs_threshold or APs_in_2 < APs_threshold:
#         if APs_in_b < APs_in_1 * 0.5:
#             continue

        APs_only_1.append(APs_in_1)
        APs_only_2.append(APs_in_2)
        common_APs.append(APs_in_b)
        physical_distances.append(physical_distance(location, l))

    # print(get_number_APs(location))
    plt.plot(physical_distances, common_APs, 'o', label = "Number of APs")
    #plt.plot(physical_distances, APs_only_1, 'o', label = "APs only in current location")
    #plt.plot(physical_distances, APs_only_2, 'o', label = "APs not in current location")

    plt.xlabel("Physical distance between provided location and all others (meters)")
    plt.ylabel("No. common Access Points")
    plt.legend()
    plt.show()



###### UJI #############3
locations = load_dataset_uji()
# norm_rss(locations)

# loc1 = int(sys.argv[1])
#plot_common_APs(locations[loc1])

#TODO 
for i in range(1, 4000, 500):
    print("Location " + str(i))
    plot_similarities(locations[i])
#     plot_common_APs(locations[i])
