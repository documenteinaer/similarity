<!-- SIMILARITY MEASUREMENT -->

In this project we try to find a similarity measurement for two given locations.
We use two datasets from zenodo:
* https://zenodo.org/record/3748719
* https://zenodo.org/record/1001662

The dataset repo is located here: https://github.com/airdocs/datasets.

The `utils.py` file reads and loads data from `dataset` repo.

Example scripts:

   


example scripts:
    * dist-lat-lon.py - ecef <=> gps transformations and distances 
    * test_pyproj.py - pyproj library test 

preprocessing.py: 
    * visualize collections 
      ` cat 2-pixel-25-02-2021_16-27-45.json | egrep "(collect|finger|wifi|gps)" `
    * apply wifi whitelist 
      ` ./preprocessing.py -i ./2-pixel-25-02-2021_16-27-45.json -wwl ./precis_wl.json -o ./2-pixel`
    * select only first direction 
       `./preprocessing.py -i ./2-pixel -o ./2.0-pixel  -cf 0`
    * select all directions 
       `./preprocessing.py -i ./2-pixel-25-02-2021_16-27-45.json -o ./2cf4  -cf 0 1 2 3`
    * generate a generic whitelist to be adjusted by hand 
      ` ./preprocessing.py -i ./2-pixel-25-02-2021_16-27-45.json -gwl -o ./wl.json `
     *  see APs present ONLY in the first file:
       `./preprocessing.py -i ./2-pixel-25-02-2021_16-27-45.json -diff ./2cf4  -o 2.diff.json`	



Step2: 
    Call `compare_locations()` function from `compare_locations.py` file


The `similarity_upb.py` script:
    similarity_collection_vs_all(json_file, collections, index = 0, method = 'Average'))

    Returns the closest neighbors that have the similarity under **0.1**.
