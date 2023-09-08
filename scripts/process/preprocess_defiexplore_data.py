"""
Script to preprocess the data from DeFi Explore for MakerDAO
"""

import json
import os

import pandas as pd
from tqdm import tqdm

from config.constants import DATA_PATH, PROCESSED_DATA_PATH

# check whether the data folder exists
if not os.path.exists(f"{PROCESSED_DATA_PATH}/defiexplore"):
    os.makedirs(f"{PROCESSED_DATA_PATH}/defiexplore")

# get a list of all files in data/defiexplore
files = os.listdir(f"{DATA_PATH}/defiexplore")

# a list to store all the data
data_lst = []

# iterate over all files
for file in tqdm(files):
    # load the json file
    with open(f"{DATA_PATH}/defiexplore/{file}", "r", encoding="utf-8") as f:
        data = json.load(f)

    # append the data to the list
    data_lst.append(pd.DataFrame(data["data"]))

# concatenate all the data
df = pd.concat(data_lst)

# save the data to the process folder
df.to_csv(f"{PROCESSED_DATA_PATH}/defiexplore/defiexplore.csv", index=False)
