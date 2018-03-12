#!/usr/bin/env bash
cd ../src/main/python/tools
pwd
python image_rebuild.py -p yiwen/size100 -t data28,data50 -p 70,30,30
python  binaryzation_cropy.py
python  dataset_build.py