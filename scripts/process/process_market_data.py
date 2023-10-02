"""
Script to process market data
"""

import pandas as pd

from config.constants import DATA_PATH
from scripts.process.process_sp import df_sp

data_dict = {
    "csv": {
        "gasprice": pd.DataFrame(),
        "etherprice": pd.DataFrame(),
    },
    "other": {
        "s&p": pd.DataFrame(),
    },
}

for var, _ in data_dict["csv"].items():
    df_data = pd.read_csv(f"{DATA_PATH}/market/{var}.csv")
    df_data.drop(columns=["UnixTimeStamp"], inplace=True)
    df_data.columns = ["date", var]
    df_data["date"] = pd.to_datetime(df_data["date"], format="%m/%d/%Y")
    df_data.sort_values(by="date", ascending=True, inplace=True)
    data_dict["csv"][var] = df_data

data_dict["other"]["s&p"] = df_sp

for type, type_dict in data_dict.items():
    for var, var_df in type_dict.items():
        df_date = pd.date_range(start=var_df["date"].min(), end=var_df["date"].max())
        var_df = var_df.set_index("date").reindex(df_date).rename_axis("date")
        var_df[var] = var_df[var].interpolate(method="ffill")
        data_dict[type][var] = var_df

df_market = data_dict["other"]["s&p"]

for _, type_dict in data_dict.items():
    for var, var_df in type_dict.items():
        if var != "s&p":
            df_market = df_market.merge(var_df, on="date", how="left")

# convert the gasprice from wei to dollar
df_market["gasprice"] = df_market["gasprice"] * df_market["etherprice"] / 1e18

# reset the index
df_market.reset_index(inplace=True)
