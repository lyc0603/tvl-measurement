"""
Script to render the balance sheet of sample protocols
"""

import pandas as pd

from config.constants import DATA_PATH
from environ.data_visualization.tab_bal import tabulate_bal

# load the balance sheet
df_bal = pd.read_csv(f"{DATA_PATH}/tvl/bal_all.csv")

for ptc_name in df_bal["protocol_name"].unique():
    # calculate the net position
    df_bal = pd.concat(
        [
            df_bal,
            pd.DataFrame(
                {
                    "protocol_name": [ptc_name],
                    "entry": ["Liabilities"],
                    "token_symbol": ["Net Position"],
                    "dollar_amount": [
                        df_bal.loc[
                            (df_bal["entry"] == "Assets")
                            & (df_bal["protocol_name"] == ptc_name),
                            "dollar_amount",
                        ].sum()
                        - df_bal.loc[
                            (df_bal["entry"] == "Liabilities")
                            & (df_bal["protocol_name"] == ptc_name),
                            "dollar_amount",
                        ].sum()
                    ],
                }
            ),
        ],
    )

    tabulate_bal(ptc_name=ptc_name, df_bal=df_bal)
