"""
Script to plot the pie chart of the composition of the DeFi protocols
"""

import matplotlib.pyplot as plt
import pandas as pd

from config.constants import DATA_PATH, FIGURES_PATH, TVL_LIST


def load_compo_data(
    load_path: str = f"{DATA_PATH}/tvl/tvl_composition_Origin.MAKER.csv",
) -> pd.DataFrame:
    """
    Function to load the composition data
    """

    print(load_path)

    return pd.read_csv(load_path)


def preprocess_compo_data(
    df_compo: pd.DataFrame,
    entity: str = "token_symbol",
    amount: str = "total_value",
    threshold: int = 6,
) -> pd.DataFrame:
    """
    Function to preprocess the composition data
    """

    # group entities and sum the amount
    df_compo = df_compo.groupby(entity).sum().reset_index()

    # sort the dataframe
    df_compo = df_compo.sort_values(by=amount, ascending=False)

    # group smaller than top 10 into "Others"
    df_compo.loc[
        df_compo[amount] < df_compo[amount].nlargest(threshold).min(), entity
    ] = "Others"

    # group the dataframe by the entity
    df_compo = df_compo.groupby(entity).sum().reset_index()

    # sort the dataframe
    df_compo = df_compo.sort_values(by=amount, ascending=False)

    print(df_compo)

    return df_compo


def plot_pie(
    df: pd.DataFrame,
    entity: str = "token_symbol",
    amount: str = "total_value",
    save_path: str = f"{FIGURES_PATH}/pie_chart_Origin.MAKER.png",
) -> None:
    """
    Function to plot the pie chart
    """

    # plot the pie chart using matplotlib
    _, ax = plt.subplots(figsize=(10, 10))
    ax.pie(
        df[amount],
        labels=df[entity],
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 25, "fontweight": "bold"},
    )

    # tight layout
    plt.tight_layout()

    # save the figure
    plt.savefig(save_path)


def plot_pie_uniswap_v2(
    save_path: str = f"{FIGURES_PATH}/pie_chart_Origin.Uniswap_V2.pdf",
) -> None:
    """
    Function to plot the pie chart
    """

    amount = [
        1.11e9,
        683.30e6,
        296.02e6,
        190.92e6,
        144.73e6,
        75.02e6,
        710010000,
    ]
    entity = ["ETH", "USDC", "WBTC", "USDT", "DAI", "FRAX", "Others"]

    # plot the pie chart using matplotlib
    _, ax = plt.subplots(figsize=(10, 10))
    ax.pie(
        amount,
        labels=entity,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 25, "fontweight": "bold"},
    )

    # tight layout
    plt.tight_layout()

    # save the figure
    plt.savefig(save_path)


if __name__ == "__main__":
    for protocol in TVL_LIST:
        # load the data
        df = load_compo_data(
            load_path=f"{DATA_PATH}/tvl/tvl_composition_Origin.{protocol}.csv"
        )

        # preprocess the data
        df = preprocess_compo_data(df)

        # plot the pie chart
        plot_pie(df, save_path=f"{FIGURES_PATH}/pie_chart_{protocol}.pdf")

    # plot the pie chart for Uniswap V2
    plot_pie_uniswap_v2()
