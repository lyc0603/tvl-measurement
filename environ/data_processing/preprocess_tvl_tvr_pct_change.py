"""
Functions to preprocess the TVL and TVR change when Ether price change
"""

import pandas as pd

DEBT_COL_NAME = "debt"
COLLATERAL_COL_NAME = "collateral"
LIQPRICE_COL_NAME = "liqPrice"
LIQRATIO_COL_NAME = "liqRatio"
ILK_NON_LIQ_PRC_COL_NAME = "nonliqPrice"
REMAINING_COLLATERAL_COL_NAME = "remainingCollateral"


def cal_vaults_value(df_ilk: pd.DataFrame, eth_price: float) -> float:
    """
    Function to calculate the vaults value
    """

    # get the collateral in different states
    df_ilk_safe = df_ilk[df_ilk[LIQPRICE_COL_NAME] <= eth_price].copy()
    df_ilk_liquidated = df_ilk[
        (df_ilk[LIQPRICE_COL_NAME] > eth_price)
        & (eth_price >= df_ilk[ILK_NON_LIQ_PRC_COL_NAME])
    ].copy()

    # calculate the remaining collateral
    df_ilk_liquidated[REMAINING_COLLATERAL_COL_NAME] = (
        df_ilk_liquidated[COLLATERAL_COL_NAME]
        - (
            (
                df_ilk_liquidated[LIQRATIO_COL_NAME] * df_ilk_liquidated[DEBT_COL_NAME]
                - df_ilk_liquidated[COLLATERAL_COL_NAME] * eth_price
            )
            / (df_ilk_liquidated[LIQRATIO_COL_NAME] - 1)
        )
        / eth_price
    )

    return (
        df_ilk_safe[COLLATERAL_COL_NAME].sum() * eth_price
        + df_ilk_liquidated[REMAINING_COLLATERAL_COL_NAME].sum() * eth_price
    )


def get_tvl_tvr_pct_change(
    df_ilk: pd.DataFrame,
    eth_price: float,
    eth_ret: float,
    liq_ratio_multiplier: float,
    ltv_multiplier: float,
    collat_multiplier: float,
) -> tuple[float, float]:
    """
    Function to calculate the TVL and TVR percentage change when Ether price change
    """

    # calculate the price that the collateral is not incentivized to liquidate
    df_ilk[ILK_NON_LIQ_PRC_COL_NAME] = (
        df_ilk[DEBT_COL_NAME] / df_ilk[COLLATERAL_COL_NAME]
    )

    # secondary factors
    df_ilk[LIQRATIO_COL_NAME] = df_ilk[LIQRATIO_COL_NAME] * liq_ratio_multiplier
    df_ilk[DEBT_COL_NAME] = df_ilk[DEBT_COL_NAME] * ltv_multiplier
    df_ilk[COLLATERAL_COL_NAME] = df_ilk[COLLATERAL_COL_NAME] * collat_multiplier

    # update the liquidation price
    df_ilk[LIQPRICE_COL_NAME] = (
        df_ilk[LIQRATIO_COL_NAME] * df_ilk[DEBT_COL_NAME] / df_ilk[COLLATERAL_COL_NAME]
    )

    ilk_total_tvl = cal_vaults_value(df_ilk=df_ilk, eth_price=eth_price)

    withdrawable_value = cal_vaults_value(
        df_ilk=df_ilk, eth_price=eth_price * (1 + eth_ret)
    )

    return withdrawable_value, ilk_total_tvl
