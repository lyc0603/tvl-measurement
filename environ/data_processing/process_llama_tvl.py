"""
Function to process the llama tvl data
"""
import json
import os

import pandas as pd
from matplotlib import pyplot as plt

from config.constants import (
    DATA_PATH,
    PROCESSED_DATA_PATH,
    FIGURES_PATH,
)
from scripts.process.process_token_lst import df_token_cate


def process_llama_tvls(
    llama_tvl_json: dict,
    slug: str,
    chain: str = "Total",
) -> tuple[dict, pd.DataFrame]:
    """
    Function to process the llama tvl data
    """

    # a dict to store the tvr
    tvl_dict = {
        "date": [],
        "protocol": [],
        "tvr": [],
        "gov": [],
        "wrap": [],
        "native": [],
        "stable": [],
    }

    if chain == "Total":
        if "tvl" not in llama_tvl_json.keys():
            return tvl_dict, pd.DataFrame()
    else:
        if chain not in llama_tvl_json["chainTvls"].keys():
            return tvl_dict, pd.DataFrame()

    # convert the data to a dataframe
    llama_tvr_df = (
        pd.DataFrame(llama_tvl_json["chainTvls"][chain]["tokensInUsd"])
        if chain != "Total"
        else pd.DataFrame(llama_tvl_json["tokensInUsd"])
    )
    llama_tvl_df = (
        pd.DataFrame(llama_tvl_json["chainTvls"][chain]["tvl"])
        if chain != "Total"
        else pd.DataFrame(llama_tvl_json["tvl"])
    )
    llama_tvl_df["protocol"] = slug

    # check the length of the dataframe
    if (len(llama_tvr_df) == 0) | (len(llama_tvl_df) == 0):
        return tvl_dict, pd.DataFrame()

    # convert the timestamp to datetime
    llama_tvr_df["date"] = pd.to_datetime(llama_tvr_df["date"], unit="s")
    llama_tvl_df["date"] = pd.to_datetime(llama_tvl_df["date"], unit="s")

    # get the unique list of symbols of defi_token_cate
    unique_symbols = df_token_cate["symbol"].unique().tolist()

    # iterate throught llama_tvl_df
    for _, row in llama_tvr_df.iterrows():
        # initialize the tvl and tvr
        tvr, gov, wrap, native, stable = 0, 0, 0, 0, 0

        # iterate through tokens
        for token, token_tvl_usd in row["tokens"].items():
            # check if the token is in the unique_symbols
            if token in unique_symbols:
                tvr += token_tvl_usd
                match df_token_cate.loc[
                    df_token_cate["symbol"] == token, "category"
                ].values[0]:
                    case "Governance Tokens":
                        gov += token_tvl_usd
                    case "Wrapped Tokens":
                        wrap += token_tvl_usd
                    case "Layer One Tokens":
                        native += token_tvl_usd
                    case "Layer Two Tokens":
                        native += token_tvl_usd
                    case "Stablecoins":
                        stable += token_tvl_usd

        tvl_dict["date"].append(row["date"])
        tvl_dict["protocol"].append(slug)
        tvl_dict["tvr"].append(tvr)
        tvl_dict["gov"].append(gov)
        tvl_dict["wrap"].append(wrap)
        tvl_dict["native"].append(native)
        tvl_dict["stable"].append(stable)

    return tvl_dict, llama_tvl_df


def process_llama_tvl(
    llama_tvl_json: dict,
    all_chain: bool = False,
    save_path: str = f"{PROCESSED_DATA_PATH}/defillama/tvl/aave-v2.csv",
    fig_path: str = f"{FIGURES_PATH}/tvr_aave-v2.pdf",
) -> None:
    """
    Function to process the llama tvl data
    """

    # check whether the path exists
    if not os.path.exists(f"{PROCESSED_DATA_PATH}/defillama/tvr"):
        os.makedirs(f"{PROCESSED_DATA_PATH}/defillama/tvr")

    # convert the data to a dataframe
    llama_tvl_df = (
        pd.DataFrame(llama_tvl_json["chainTvls"]["Ethereum"]["tokensInUsd"])
        if not all_chain
        else pd.DataFrame(llama_tvl_json["tokensInUsd"])
    )

    # convert the timestamp to datetime
    llama_tvl_df["date"] = pd.to_datetime(llama_tvl_df["date"], unit="s")

    # get the unique list of symbols of defi_token_cate
    unique_symbols = df_token_cate["symbol"].unique().tolist()

    # iterate throught llama_tvl_df
    for _, row in llama_tvl_df.iterrows():
        # initialize the tvl and tvr
        tvl, tvr, gov, wrap, native, stable = 0, 0, 0, 0, 0, 0

        # iterate through tokens
        for token, token_tvl_usd in row["tokens"].items():
            # check if the token is in the unique_symbols
            if token in unique_symbols:
                tvr += token_tvl_usd

                match df_token_cate.loc[
                    df_token_cate["symbol"] == token, "category"
                ].values[0]:
                    case "Governance Tokens":
                        gov += token_tvl_usd
                    case "Wrapped Tokens":
                        wrap += token_tvl_usd
                    case "Layer One Tokens":
                        native += token_tvl_usd
                    case "Layer Two Tokens":
                        native += token_tvl_usd
                    case "Stablecoins":
                        stable += token_tvl_usd

        llama_tvl_df.loc[llama_tvl_df["date"] == row["date"], "tvr"] = tvr
        llama_tvl_df.loc[llama_tvl_df["date"] == row["date"], "tvl"] = tvl
        llama_tvl_df.loc[llama_tvl_df["date"] == row["date"], "gov"] = gov
        llama_tvl_df.loc[llama_tvl_df["date"] == row["date"], "wrap"] = wrap
        llama_tvl_df.loc[llama_tvl_df["date"] == row["date"], "native"] = native
        llama_tvl_df.loc[llama_tvl_df["date"] == row["date"], "stable"] = stable

    # save the llama tvl data
    llama_tvl_df.to_csv(save_path, index=False)

    # plot both the tvl and tvr
    plt.plot(llama_tvl_df["date"], llama_tvl_df["tvl"], label="tvl")
    plt.plot(llama_tvl_df["date"], llama_tvl_df["tvr"], label="tvr")
    plt.legend()

    # rotate the xticks by 45 degrees
    plt.xticks(rotation=45)

    # tight layout
    plt.tight_layout()

    # save the plot
    plt.savefig(fig_path, dpi=300)

    # close the plot
    plt.close()


def process_llama_treasury(
    llama_treasury_json: dict,
    save_path: str = f"{PROCESSED_DATA_PATH}/defillama/treasury/yearn-finance.csv",
    fig_path: str = f"{FIGURES_PATH}/treasury_yearn-finance.pdf",
) -> None:
    """
    Function to process the llama treasury data
    """

    # check whether the path exists
    if not os.path.exists(f"{PROCESSED_DATA_PATH}/defillama/treasury"):
        os.makedirs(f"{PROCESSED_DATA_PATH}/defillama/treasury")

    # convert the data to a dataframe
    llama_tvl_df = pd.DataFrame(
        llama_treasury_json["chainTvls"]["Ethereum"]["tokensInUsd"]
    )

    # convert the timestamp to datetime
    llama_tvl_df["date"] = pd.to_datetime(llama_tvl_df["date"], unit="s")

    # get the unique list of symbols of defi_token_cate
    unique_symbols = df_token_cate["symbol"].unique().tolist()

    # iterate throught llama_tvl_df
    for _, row in llama_tvl_df.iterrows():
        # initialize the tvl and tvr
        tvl, tvr = 0, 0

        # iterate through tokens
        for token, token_tvl_usd in row["tokens"].items():
            tvl += token_tvl_usd

            # check if the token is in the unique_symbols
            if token in unique_symbols:
                tvr += token_tvl_usd

        llama_tvl_df.loc[llama_tvl_df["date"] == row["date"], "tvr"] = tvr
        llama_tvl_df.loc[llama_tvl_df["date"] == row["date"], "tvl"] = tvl

    # save the llama tvl data
    llama_tvl_df.to_csv(save_path, index=False)

    # plot both the tvl and tvr
    plt.plot(llama_tvl_df["date"], llama_tvl_df["tvl"], label="tvl")
    plt.plot(llama_tvl_df["date"], llama_tvl_df["tvr"], label="tvr")
    plt.legend()

    # rotate the xticks by 45 degrees
    plt.xticks(rotation=45)

    # tight layout
    plt.tight_layout()

    # save the plot
    plt.savefig(fig_path, dpi=300)

    # close the plot
    plt.close()


def process_llama_lst(
    protocol_lst_json: dict,
) -> list[str]:
    """
    Function to process the llama list data
    """

    return [_["slug"] for _ in protocol_lst_json]


if __name__ == "__main__":
    # load the llama tvl data
    with open(
        f"{DATA_PATH}/defillama/tvl/makerdao.json", "r", encoding="utf-8"
    ) as target_file:
        llama_tvl_json = json.load(target_file)

    # process the llama tvl data
    process_llama_tvl(
        llama_tvl_json=llama_tvl_json,
        all_chain=True,
        save_path=f"{PROCESSED_DATA_PATH}/defillama/tvr/makerdao.csv",
        fig_path=f"{FIGURES_PATH}/tvr_makerdao.pdf",
    )

    with open(
        f"{DATA_PATH}/defillama/treasury/yearn-finance.json", "r", encoding="utf-8"
    ) as target_file:
        llama_treasury_json = json.load(target_file)

    # process the llama treasury data
    process_llama_treasury(
        llama_treasury_json=llama_treasury_json,
        save_path=f"{PROCESSED_DATA_PATH}/defillama/treasury/yearn-finance.csv",
        fig_path=f"{FIGURES_PATH}/treasury_yearn-finance.pdf",
    )
