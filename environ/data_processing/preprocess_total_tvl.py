"""
Function to preprocess total TVL data
"""
import pandas as pd
from config.constants import (
    PROCESSED_DATA_PATH,
)
from config.constants import END_OF_SAMPLE_PERIOD

REMOVE_PROTOCOLS = ["binance-cex"]


def preprocess_total_tvl(
    df_path: str = f"{PROCESSED_DATA_PATH}/defillama/defillama_tvl_all.csv",
) -> pd.DataFrame:
    """
    Function to preprocess total TVL data
    """

    # load the total tvl data
    df_tvl_all = pd.read_csv(df_path)

    # remove the protocols
    df_tvl_all = df_tvl_all[~df_tvl_all["protocol"].isin(REMOVE_PROTOCOLS)]

    # convert the timestamp to datetime
    df_tvl_all["date"] = pd.to_datetime(df_tvl_all["date"])

    # sort the dataframe by protocol and date
    df_tvl_all = df_tvl_all.sort_values(by=["protocol", "date"], ascending=True)

    # convert the date to %Y-%m-%d
    df_tvl_all["date"] = df_tvl_all["date"].dt.strftime("%Y-%m-%d")

    # drop the duplicates according to date
    df_tvl_all = df_tvl_all.drop_duplicates(subset=["date", "protocol"], keep="first")

    # convert the date to datetime
    df_tvl_all["date"] = pd.to_datetime(df_tvl_all["date"])

    # only keep the data before 2023-07-01
    df_tvl_all = df_tvl_all[df_tvl_all["date"] < END_OF_SAMPLE_PERIOD]

    # sum the tvl and tvr of the same date
    df_tvl_all = df_tvl_all.groupby(["date"]).sum().reset_index()

    return df_tvl_all
