"""
Script to fetch the money supply data from FRED
"""

from config.constants import DATA_PATH, FRED_API_KEY
import requests


series_type = "M2SL"
url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_type}&api_key={FRED_API_KEY}"
