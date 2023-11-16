#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  echo "usage: setup-db.sh /path/to/data"
  exit 1
fi

data_path="$1"
echo "Using data in $data_path"

echo "Inserting all Compound events"
find "$data_path/compound" -name "*.jsonl.gz" -print0 | xargs -0 gzcat | mongoimport --db=tvl-measurement --collection=events 