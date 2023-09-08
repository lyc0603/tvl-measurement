"""
Script to generate the balance sheets of sample protocols to implement the risk analysis
"""

from config.constants import DATA_PATH
from environ.data_processing.preprocess_bal_ptc import (
    preprocess_aave_v3_bal,
    preprocess_makerdao_bal,
)

df_makerdao = preprocess_makerdao_bal()
df_aave_v3 = preprocess_aave_v3_bal()

df_aave_v3.to_csv(f"{DATA_PATH}/tvl/bal_aave_v3.csv", index=False)
df_makerdao.to_csv(f"{DATA_PATH}/tvl/bal_makerdao.csv", index=False)
