"""
Script to plot the sensitivity test results of protocol
"""

import matplotlib.pyplot as plt
import pandas as pd

from config.constants import DATA_PATH, FIGURES_PATH, SAMPLE_SYSTEM_TOKEN
from environ.data_fetching.lido_data_fetching import get_total_pooled_ether_lido
from environ.data_fetching.token_price import get_eth_price
from scripts.process.process_risk_analysis import results

# set the figure size
plt.figure(figsize=(5, 2))

df_makerdao = pd.read_csv(f"{DATA_PATH}/tvl/bal_makerdao.csv")

tvl_dict = {
    "MakerDAO": df_makerdao.loc[
        df_makerdao["entries"] == "Reserve Token", "dollar_amount"
    ].sum(),
    "Lido": get_total_pooled_ether_lido() * get_eth_price(),
}


df_sensitivity_test = pd.DataFrame(results)
df_sensitivity_test = df_sensitivity_test.loc[
    df_sensitivity_test["pool"].isin(SAMPLE_SYSTEM_TOKEN)
].copy()

plot_dict = {
    "protocol": [],
    "price_pct": [],
    "tvl": [],
}

for protocol in df_sensitivity_test["protocol"].unique():
    df_protocol = df_sensitivity_test[
        df_sensitivity_test["protocol"] == protocol
    ].copy()

    for price_pct in df_protocol["price_pct"].unique():
        df_price_pct = df_protocol[df_protocol["price_pct"] == price_pct].copy()

        # get the total tvl
        tvl = tvl_dict[protocol] - df_price_pct["tvl_drop"].sum()

        # append the results to the dict
        plot_dict["protocol"].append(protocol)
        plot_dict["price_pct"].append(price_pct)
        plot_dict["tvl"].append(tvl)

# sum up the results
df_plot = pd.DataFrame(plot_dict)

for protocol in df_plot["protocol"].unique():
    df_protocol = df_plot[df_plot["protocol"] == protocol].copy()

    # plot the results
    plt.plot(
        df_protocol["price_pct"],
        df_protocol["tvl"],
        label=f"{protocol}",
    )

# show the legend on the upper left corner
plt.legend(loc="upper left")

# add the grid and increase the opacity and increase the intensity
plt.grid(alpha=0.3)

# x and y labels
plt.xlabel("Percentage of price drop of ETH")

# set the y label
plt.ylabel("Total TVL")

# tight layout
plt.tight_layout()

plt.savefig(f"{FIGURES_PATH}/protocol_tvl_drop.pdf", dpi=300)
