"""
Script to tabulate the summary statistics
"""

from environ.data_processing.sum_stats import describe_df
from config.constants import TABLES_PATH

# convert the count column to int
describe_df["count"] = describe_df["count"].apply(lambda x: f"{int(x):,}")

# other two decimal places
for col in describe_df.columns[1:]:
    describe_df[col] = describe_df[col].apply(lambda x: f"{x:.1e}")

# replace % to \% in columns
describe_df.columns = describe_df.columns.str.replace("%", "\%")

# save the latex table
with open(f"{TABLES_PATH}/sum_stats.tex", "w", encoding="utf-8") as target_file:
    target_file.write(describe_df.to_latex(escape=False, index=True))
