"""
Script to plot the collateral ratio
"""

import matplotlib.pyplot as plt

from scripts.process.process_risk_analysis import bal_makerdao

# plot the collateral ratio
plt.figure(figsize=(12, 8))

lst_collat = 0

for idx in bal_makerdao["idx"].unique():
    bal_makerdao.loc[(bal_makerdao["idx"] == idx), "collat_ratio"]
