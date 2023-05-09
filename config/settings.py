"""
Project settings
"""

from os import path

PROJECT_ROOT = path.dirname(path.dirname(__file__))

CACHE_path = path.join(PROJECT_ROOT, "cache")
DISK_CACHE = True
