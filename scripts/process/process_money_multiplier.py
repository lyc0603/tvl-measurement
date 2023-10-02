"""
Script to calculate the money multiplier from the money supply data
"""

import datetime
import json

from config.constants import DATA_PATH

monetary_data_dict = {
    "M0": {
        "date": [],
        "value": [],
    },
    "M2": {
        "date": [],
        "value": [],
    },
}

for series_name, _ in monetary_data_dict.items():
    # load the data
    with open(f"{DATA_PATH}/fred/{series_name}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # save the data into the dictionary
    for obs in data["observations"]:
        monetary_data_dict[series_name]["date"].append(obs["date"])
        monetary_data_dict[series_name]["value"].append(float(obs["value"]))

# convert the money base data into billions
for i in range(len(monetary_data_dict["M0"]["value"])):
    monetary_data_dict["M0"]["value"][i] /= 1000

# a dictionary to store the money multiplier data
money_multiplier_dict = {
    "date": [],
    "value": [],
}

# calculate the money multiplier
for i in range(len(monetary_data_dict["M0"]["value"])):
    money_multiplier_dict["date"].append(monetary_data_dict["M0"]["date"][i])
    money_multiplier_dict["value"].append(
        monetary_data_dict["M2"]["value"][i] / monetary_data_dict["M0"]["value"][i]
    )

# convert the date into datetime objects and less one month
for i in range(len(money_multiplier_dict["date"])):
    money_multiplier_dict["date"][i] = datetime.datetime.strptime(
        money_multiplier_dict["date"][i], "%Y-%m-%d"
    )
