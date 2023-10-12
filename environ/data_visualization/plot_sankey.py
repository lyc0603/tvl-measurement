"""
Function to plot the sankey diagram
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

from config import constants

pio.kaleido.scope.mathjax = None

COLOR_DICT = {
    # Dai Stablecoin (DAI)
    "0x6b175474e89094c44da98b954eedeac495271d0f": "rgba(255,162,0,0.4)",
    # Curve.fi DAI/USDC/USDT (3Crv)
    "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490": "rgba(55,178,255,0.4)",
    # Uniswap DAI/USDC LP
    "0xae461ca67b15dc8dc81ce7615e0320da1a9ab8d5": "rgba(252,65,94,0.4)",
}

NODE_COLOR_DICT = {
    "MakerDAO": "rgba(255,162,0,0.7)",
    "Uniswap V2": "rgba(252,65,94,0.7)",
    "Uniswap V3": "rgba(252,65,94,0.7)",
    "Balancer": "rgba(0,0,0,0.7)",
    "Curve V1": "rgba(55,178,255,0.7)",
    "Aave V2": "rgba(136,102,255,0.7)",
    "Compound V2": "rgba(34,136,0,0.7)",
    "Yearn": "rgba(0,0,255,0.7)",
}


def process_flow_usd_data(
    df_data: pd.DataFrame,
    amount_col: str = "flow_usd",
) -> pd.DataFrame:
    """
    Function to preprocess the flow usd data
    """

    # preprocess the contract column
    for token in df_data["contract"].unique().tolist():
        if token not in COLOR_DICT.keys():
            df_data.loc[df_data["contract"] == token, "contract"] = "Others"

    # groupby the source and target
    df_data = (
        df_data.groupby(["source", "target", "contract"])
        .agg({amount_col: "sum"})
        .reset_index()
    )

    # set the token color
    df_data["token_color"] = "rgba(128,128,128,0.4)"
    for key, value in COLOR_DICT.items():
        df_data.loc[df_data["contract"] == key, "token_color"] = value

    return df_data


def plot_sankey(
    df_data: pd.DataFrame,
    save_path: str = f"{constants.FIGURES_PATH}/sankey_amount.pdf",
    source_col: str = "source",
    target_col: str = "target",
    amount_col: str = "amount",
    # link_color_col: str = "token_color",
) -> None:
    """
    Function to plot the sankey diagram
    """

    # get the unique list of protocols
    source_node = df_data[source_col].unique().tolist()
    target_node = df_data[target_col].unique().tolist()
    unique_lst = [f"{i}_S" for i in source_node] + [f"{i}_T" for i in target_node]
    # token_color_lst = df_data[link_color_col].values.tolist()
    node_color_lst = [NODE_COLOR_DICT[i] for i in source_node] + [
        NODE_COLOR_DICT[i] for i in target_node
    ]

    # lists for sankey
    source_lst = []
    target_lst = []
    amount_lst = []

    # iterate through the df_data
    for _, row in df_data.iterrows():
        source_lst.append(unique_lst.index(f"{row[source_col]}_S"))
        target_lst.append(unique_lst.index(f"{row[target_col]}_T"))
        amount_lst.append(row[amount_col])

    # color dict for the sankey
    color_lst = ["rgba(0,119,179,0.8)" for _ in range(len(source_node))] + [
        "rgba(0,119,179,0.8)" for _ in range(len(target_node))
    ]

    # remove the S and T from the unique list
    unique_lst = [i[:-2] for i in unique_lst]

    # create the sankey diagram
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    # line=dict(color="black", width=0.5),
                    label=unique_lst,
                    color=node_color_lst,
                ),
                link=dict(
                    source=source_lst,
                    target=target_lst,
                    value=amount_lst,
                    # color=token_color_lst,
                ),
            )
        ]
    )

    # save the figure
    fig.write_image(save_path, format="pdf")


if __name__ == "__main__":
    pass
