#!/bin/bash
cd src/main/python
echo "come in to path:  `pwd`"
echo "starting to running clustering module"
#`python  __init__.py`
#dataset=("flame" "path" "aggregation"  "unblance"  "path_integer" "compound" "d31" "r15" "spiral" "pathbased" "jain")
dataset=("flame" "path" "aggregation"  "unblance"  "path_integer" "compound"  "spiral" "pathbased" )
dataset=("path" "flame" "unblance" "aggregation")

python main.py -f unblance

# python -m cProfile -s cumulative main.py -f
# aggregation
# compound
# d31
# flame
# r15
# spiral
# unbalance
# pathbased
# jain