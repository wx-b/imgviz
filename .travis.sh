#!/bin/bash

set -e
set -x

pytest -v tests

MPLBACKEND=agg python getting_started.py
for f in examples/*.py; do
  MPLBACKEND=agg python $f
done
