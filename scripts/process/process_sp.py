"""
Script to process the S&P index
"""

import pandas as pd
from config.constants import DATA_PATH


df_sp = pd.read_excel(
    f"{DATA_PATH}/market/PerformanceGraphExport.xls",
    index_col=None,
    skiprows=6,
    skipfooter=4,
    # usecols="A:B:C",
)
df_sp.columns = ["date", "s&p"]
df_sp["date"] = pd.to_datetime(df_sp["date"])
df_sp.sort_values(by="date", ascending=True, inplace=True)
