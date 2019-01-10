import numpy as np
 
from pyspark import SparkContext
from pyspark import SparkConf
 
conf = SparkConf()
conf.setMaster("spark://master:7077")
conf.setAppName("NumpyMult")
sc = SparkContext(conf=conf)
 
def mult(x):
    y = np.array([2])
    return x*y
 
x = np.arange(10000)
distData = sc.parallelize(x)
 
results = distData.map(mult).collect()
 
print(results)
