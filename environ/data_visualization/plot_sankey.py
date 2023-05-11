"""
Function to plot the sankey diagram
"""

import pandas as pd

import plotly.graph_objects as go
from config import constants


def plot_sankey(
    df_data: pd.DataFrame,
    save_path: str = f"{constants.FIGURES_PATH}/sankey_amount.pdf",
) -> None:
    """
    Function to plot the sankey diagram
    """

    # groupby the source and target
    df_data = df_data.groupby(["source", "target"]).sum().reset_index()

    # get the unique list of protocols
    source_node = df_data["source"].unique().tolist()
    target_node = df_data["target"].unique().tolist()
    unique_lst = [f"{i}_S" for i in source_node] + [f"{i}_T" for i in target_node]

    # lists for sankey
    source_lst = []
    target_lst = []
    amount_lst = []

    # iterate through the df_data
    for _, row in df_data.iterrows():
        source_lst.append(unique_lst.index(f"{row['source']}_S"))
        target_lst.append(unique_lst.index(f"{row['target']}_T"))
        amount_lst.append(row["amount"])

    # color dict for the sankey
    color_lst = ["blue" for i in range(len(source_node))] + [
        "yellow" for i in range(len(target_node))
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
                    line=dict(color="black", width=0.5),
                    label=unique_lst,
                    color=color_lst,
                ),
                link=dict(
                    source=source_lst,
                    target=target_lst,
                    value=amount_lst,
                ),
            )
        ]
    )

    # save the figure
    fig.write_image(save_path)
