"""
Scripts to process the fred data
"""

import json
import pandas as pd

from config.constants import DATA_PATH

# a dict to store the data
data_dict = {
    "monthly": {
        "CPI": pd.DataFrame(),
    },
    "daily": {
        "FFER": pd.DataFrame(),
        "VIX": pd.DataFrame(),
    },
}

for freq, freq_data in data_dict.items():
    for var, _ in freq_data.items():
        with open(f"{DATA_PATH}/fred/{var}.json", "r", encoding="utf-8") as f:
            # load the data
            df_data = pd.DataFrame(json.load(f)["observations"])
            df_data["date"] = pd.to_datetime(df_data["date"])
            df_data = df_data[["date", "value"]]

            if freq == "daily":
                pd_date = pd.date_range(
                    start=df_data["date"].min(), end=df_data["date"].max()
                )
                # expand the dataframe to include all dates
                df_data = df_data.set_index("date").reindex(pd_date).rename_axis("date")

                # fill in the missing values
                df_data["value"] = df_data["value"].interpolate(method="ffill")

            df_data.rename(columns={"value": var}, inplace=True)
            data_dict[freq][var] = df_data

# use the CPI as the base dataframe to merge the other dataframes
df_fred = data_dict["monthly"]["CPI"]

for freq, freq_data in data_dict.items():
    for var, _ in freq_data.items():
        if var != "CPI":
            df_fred = df_fred.merge(data_dict[freq][var], on="date", how="left")
