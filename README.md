<!-- SIMILARITY MEASUREMENT -->

In this project we try to find a similarity measurement for two given locations.
We use two datasets from zenodo:
* https://zenodo.org/record/3748719
* https://zenodo.org/record/1001662

The dataset repo is located here: https://github.com/airdocs/datasets.

The `utils.py` file reads and loads data from `dataset` repo.

    costincarabas@MacBook:~/facultate/doctorat/research/AirDocs$ tree -L 2
    ..
    ├── datasets
    │   ├── DISTRIBUTED_OPENSOURCE_version2
    │   ├── README.md
    │   └── UJI_LIB_DB_v2.2
    └── similarity
        ├── README.md
        ├── __pycache__
        ├── similarity.py
        └── utils.py


Step1:
    * Requires `whitelist.txt`
    * Outputs `p_6-redmi-17-03-2021_12-52-29.json`

    `python3 preprocessing.py 6-redmi-17-03-2021_12-52-29.json`

Step2: 
    Call `compare_locations()` function from `compare_locations.py` file


The `similarity_upb.py` script:
    similarity_collection_vs_all(json_file, collections, index = 0, method = 'Average'))

    Returns the closest neighbors that have the similarity under **0.1**.
