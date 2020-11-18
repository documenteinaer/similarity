<!-- SIMILARITY MEASUREMENT -->

In this project we try to find a similarity measurement for two given locations.
We use two datasets from zenodo:
* https://zenodo.org/record/3748719
* https://zenodo.org/record/1001662

The dataset repo is located here: https://github.com/airdocs/datasets.

The `utils.py` file reads and loads data from `dataset` repo.

.. code-block:

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
