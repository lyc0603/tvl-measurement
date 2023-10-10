"""
Function to preprocess total TVL data
"""
import pandas as pd

from config.constants import END_OF_SAMPLE_PERIOD, PROCESSED_DATA_PATH
from environ.data_fetching.fetch_llama_tvl import fetch_llama_total_tvl

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

    # keep data after 2019-06-01
    df_tvl_all = df_tvl_all[df_tvl_all["date"] >= "2019-06-01"]

    return df_tvl_all


def preprocess_ptc_tvl(
    chain: str,
) -> pd.DataFrame:
    """
    Function to preprocess protocol TVL data
    """

    # load the total tvl data
    total_tvl_eth_without_double_counting = fetch_llama_total_tvl(
        chain=chain,
    )

    # convert json to dataframe
    total_tvl_eth_without_double_counting_df = pd.DataFrame(
        total_tvl_eth_without_double_counting
    )

    # convert the timestamp to datetime
    total_tvl_eth_without_double_counting_df["date"] = pd.to_datetime(
        total_tvl_eth_without_double_counting_df["date"],
        unit="s",
    )

    # only keep the data before 2023-07-01
    total_tvl_eth_without_double_counting_df = total_tvl_eth_without_double_counting_df[
        total_tvl_eth_without_double_counting_df["date"] < END_OF_SAMPLE_PERIOD
    ]

    # load the total tvl data
    df_tvl_all = preprocess_total_tvl(
        df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvl_all_{chain}.csv"
    )[["date", "totalLiquidityUSD"]]

    # load the total tvr data
    df_tvr_all = preprocess_total_tvl(
        df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvr_all_{chain}.csv"
    )[["date", "tvr"]]

    # merge the dataframes
    df_agg = pd.merge(
        df_tvl_all,
        df_tvr_all,
        on="date",
        how="outer",
    )
    df_agg = pd.merge(
        df_agg,
        total_tvl_eth_without_double_counting_df,
        on="date",
        how="outer",
    )

    return df_agg


if __name__ == "__main__":
    df = preprocess_ptc_tvl(
        chain="Mixin",
    )

    df.loc[
        (df["date"] >= "2022-11-06") & (df["date"] <= "2022-11-08"),
        "totalLiquidityUSD",
    ] = df.loc[
        (df["date"] == "2022-11-05"),
        "totalLiquidityUSD",
    ].values[
        0
    ]

    # show the date if the totalLiquidityUSD is NaN
    print(df[df["totalLiquidityUSD"].isna()])
