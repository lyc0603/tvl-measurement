"""
Functions to preprocess the TVL and TVR change when Ether price change
"""

import pandas as pd

DEBT_COL_NAME = "debt"
COLLATERAL_COL_NAME = "collateral"
LIQPRICE_COL_NAME = "liqPrice"
ILK_NON_LIQ_PRC_COL_NAME = "ilk_non_liq_prc"


def get_tvl_tvr_pct_change(
    df_ilk: pd.DataFrame,
    eth_price: float,
    eth_ret: float,
) -> tuple[float, float]:
    """
    Function to calculate the TVL and TVR percentage change when Ether price change
    """

    # calculate the price that the collateral is not incentivized to liquidate
    df_ilk[ILK_NON_LIQ_PRC_COL_NAME] = (
        df_ilk[DEBT_COL_NAME] / df_ilk[COLLATERAL_COL_NAME]
    )

    # iterate from ilk price to highest liq price
    ilk_price = eth_price * (1 + eth_ret)

    # get the collateral in different states currently
    df_ilk_safe_current = df_ilk[df_ilk[LIQPRICE_COL_NAME] <= eth_price].copy()
    df_ilk_liquidated_current = df_ilk[
        (df_ilk[LIQPRICE_COL_NAME] > eth_price)
        & (eth_price >= df_ilk[ILK_NON_LIQ_PRC_COL_NAME])
    ].copy()

    # get the total collateral
    ilk_total_tvl = (
        df_ilk_safe_current[COLLATERAL_COL_NAME].sum() * eth_price
        + df_ilk_liquidated_current[DEBT_COL_NAME].sum()
    )

    # get the collateral in different states
    df_ilk_safe = df_ilk[df_ilk[LIQPRICE_COL_NAME] <= ilk_price].copy()
    df_ilk_liquidated = df_ilk[
        (df_ilk[LIQPRICE_COL_NAME] > ilk_price)
        & (ilk_price >= df_ilk[ILK_NON_LIQ_PRC_COL_NAME])
    ].copy()

    # calculate the withdrawable value
    withdrawable_value = (
        df_ilk_safe[COLLATERAL_COL_NAME].sum() * ilk_price
        + df_ilk_liquidated[DEBT_COL_NAME].sum()
    )

    return withdrawable_value, ilk_total_tvl
