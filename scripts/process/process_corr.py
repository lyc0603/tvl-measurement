"""
Script to process the correlation panel
"""

import pandas as pd

from config.constants import CORR_NAMING_DICT
from scripts.process.process_fred_data import df_fred
from scripts.process.process_leverage_ratio import leverage_ratio_dict
from scripts.process.process_money_multiplier import money_multiplier_dict
from scripts.process.process_market_data import df_market


df_leverage = pd.DataFrame(leverage_ratio_dict).rename(columns={"value": "leverage"})
df_multiplier = pd.DataFrame(money_multiplier_dict).rename(
    columns={"value": "multiplier"}
)

# merge the fred and market data
df_corr = df_fred.merge(df_market, on="date", how="left")

# merge the leverage ratio data
df_corr = df_corr.merge(df_leverage, on="date", how="left")

# merge the money multiplier data
df_corr = df_corr.merge(df_multiplier, on="date", how="left")

# only keep the data after 2021 and before the max date of the leverage ratio data
df_corr = df_corr[df_corr["date"] >= "2021-01-01"]
df_corr = df_corr[df_corr["date"] <= df_leverage["date"].max()]

# drop the date column
df_corr = df_corr.drop(columns=["date"])

# rename the columns
df_corr = df_corr.rename(columns=CORR_NAMING_DICT)

# convert the data to float
df_corr = df_corr.astype(float)
