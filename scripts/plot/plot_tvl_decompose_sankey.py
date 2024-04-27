"""
Script to plot the TVL decomposition sankey plot
"""

import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

from scripts.process.process_tvl_decompose_sankey import TVL_DECOMPOSE_SANKEY_DICT
from config.constants import FIGURES_PATH, SAMPLE_DATA_DICT

# enlarge the font size
plt.rcParams.update({"font.size": 16})

for snapshot, date_dict in TVL_DECOMPOSE_SANKEY_DICT.items():
    fig = plt.figure(figsize=(10, 5))
    ax_df = fig.add_subplot(1, 1, 1, xticks=[], yticks=[])
    sankey = Sankey(
        ax=ax_df, scale=0.01, offset=0.2, head_angle=180, format="%.1f", unit="%"
    )
    sankey.add(
        flows=date_dict["flows"][0],
        labels=date_dict["labels"][0],
        orientations=date_dict["orientations"][0],
        patchlabel="TVL",
        # pathlengths=[0.01] * len(flows_list),
    )
    sankey.add(
        flows=date_dict["flows"][1],
        labels=date_dict["labels"][1],
        orientations=date_dict["orientations"][1],
        # patchlabel="TVR",
        prior=0,
        connect=(5, 0),
    )
    diagrams = sankey.finish()

    diagrams[0].texts[1].set_position(xy=[-1, 0.95])
    diagrams[0].texts[2].set_position(xy=[-1, -0.95])
    # diagrams[1].texts[2].set_position(xy=[2.3, 0.3355696919097503])

    # tight layout
    plt.tight_layout()

    # remove the frame
    plt.box(False)

    fig.savefig(f"{FIGURES_PATH}/tvl_decompose_sankey_{snapshot}.pdf", dpi=300)
