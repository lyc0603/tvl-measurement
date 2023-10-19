"""
Script to process summary statistics
"""

import json
from glob import glob

import pandas as pd
from tqdm import tqdm

from config.constants import DATA_PATH

TIMESTAMP = 1688169600

CHAIN_PTC_DICT = {}
CHAIN_TVL_DICT = {}
CHAIN_TOKEN_DICT = {}

ptc_tvl_agg_df = pd.DataFrame()

# iterate through all the files in DATA_PATH/defillama/tvl
for file in tqdm(glob(f"{DATA_PATH}/defillama/tvl/*.json")):
    # load the json file
    with open(file, "r", encoding="utf-8") as target_file:
        data_json = json.load(target_file)
    ptc_tvl_df = pd.DataFrame(data_json["tvl"])
    ptc_tvl_df["protocol"] = file.split("/")[-1].split(".")[0]
    ptc_tvl_agg_df = pd.concat([ptc_tvl_agg_df, ptc_tvl_df])

# remove negative tvl
ptc_tvl_agg_df = ptc_tvl_agg_df.loc[ptc_tvl_agg_df["totalLiquidityUSD"] > 0]

# drop non day end
ptc_tvl_agg_df["date"] = pd.to_datetime(ptc_tvl_agg_df["date"], unit="s")
ptc_tvl_agg_df.sort_values(["protocol", "date"], inplace=True)
ptc_tvl_agg_df["date"] = ptc_tvl_agg_df["date"].dt.strftime("%Y-%m-%d")
ptc_tvl_agg_df.drop_duplicates(["protocol", "date"], keep="first", inplace=True)
ptc_tvl_agg_df["totalLiquidityUSD"].describe().reset_index(name="totalLiquidityUSD")

describe_df = pd.DataFrame()
describe_df = pd.concat(
    [
        describe_df,
        ptc_tvl_agg_df["totalLiquidityUSD"].describe().to_frame().T,
        ptc_tvl_agg_df.groupby(["date"])["totalLiquidityUSD"]
        .sum()
        .describe()
        .to_frame()
        .T,
        ptc_tvl_agg_df.groupby(["protocol"])["totalLiquidityUSD"]
        .mean()
        .describe()
        .to_frame()
        .T,
    ]
)
describe_df.index = pd.Index(["$TVL_{i,t}$", "$TVL_{t}$", "$\\bar{TVL}_{i}$"])
