# clusterfinder
Python module for cluster arithmetic.


# 目录
- conf 项目配置目录
- data 项目数据目录
- distance 求距离目录
A cluster framework for 'Clustering by fast search and find of density peaks' in science 2014.

## How to Use

# Dependencies
Step0: If your data is not the distance between points but the points' vector, write you distance builder in distance like distance_builder_data_iris_flower.py.
Step1: Change the data file in step1_choose_center.py, then run it to choose cluster threshold.
Step2: Change the data file and threshold in step2_cluster.py, then run it.
```python
python distance_builder_data_iris_flower.py
python step1_choose_center.py
python step2_cluster.py
```

-    [NumPy](http://www.numpy.org/): normal computing
-    [Matplotlib](http://matplotlib.sourceforge.net/): For plotting data to choose threshold
-    [Scikit-Learn](https://github.com/scikit-learn/scikit-learn): use for mds to plot result
## Dependencies
- [NumPy](http://www.numpy.org): normal computing
- [Matplotlib](http://matplotlib.sourceforge.net/): For plotting data to choose threshold
- [Scikit-Learn](https://github.com/scikit-learn/scikit-learn): use for mds to plot result

## Reference
- [Clustering by fast search and find of density peaks](http://www.sciencemag.org/content/344/6191/1492.full)

# References
- Python Resource
  - [Dcluster](https://github.com/GuipengLi/Dcluster.git)
  - [DensityPeakCluster](https://github.com/jasonwbw/DensityPeakCluster.git)
- Mainly Paper
  - [Cluster by fast search and find density peaks](http://www.sciencemag.org/content/344/6191/1492.full)
## License
The MIT License (MIT)
