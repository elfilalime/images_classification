import numpy as np
import pandas as pd
import pickle
import io
import time
from pyspark import SparkContext
from pyspark import SparkConf


import sys

conf = SparkConf()
conf.setMaster("spark://0.0.0.0:7077")
conf.setAppName("NumpyMult")
sc = SparkContext(conf=conf)

def addToServer(image):
	from elasticsearch import Elasticsearch
	from minio import Minio
	from minio.error import ResponseError

	es = Elasticsearch(['http://elasticsearch:9200'])
	minioClient = Minio('minio:9000',access_key='minio',secret_key='minio123',secure=False)
	ret = ""
	try:
		t = time.time()
		buf = pickle.dumps(image[0])

		if not minioClient.bucket_exists('dat'):
			minioClient.make_bucket('dat')

		minioClient.put_object('dat', str(t)+".npy", io.BytesIO(buf),len(buf))

		doc = {
		    'image': str(t)+".npy",
		    'label': str(image[1])
		}
		
		es.index(index="images_classification", doc_type='images',body=doc)
		
		ret = t
	except :
		
		ret = 0

	return ret

label = np.load(sys.argv[2])
data = np.load(sys.argv[1], mmap_mode='r')

dct = {'data': list(data),'label':list(label)}

dat = pd.DataFrame(dct).values

distData = sc.parallelize(dat)

s = distData.map(addToServer).collect()

print(s)

