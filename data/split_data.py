import numpy as np
import pandas as pd
import io
from minio import Minio
from minio.error import ResponseError
import time
from pyspark import SparkContext
from pyspark import SparkConf
from elasticsearch import Elasticsearch

conf = SparkConf()
conf.setMaster("spark://master:7077")
conf.setAppName("NumpyMult")
sc = SparkContext(conf=conf)


def addToServer(image):
	es = Elasticsearch(['http://elasticsearch:9200'])
	minioClient = Minio('minio:9000',access_key='minio',secret_key='minio123',secure=False)
	ret = ""
	try:
		t = time.time()
		buf = image[0].tobytes()

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

data = np.load('/home/train.npy')
label = np.load('/home/train_labels.npy')

dct = {'data': list(data),'label':list(label)}

dat = pd.DataFrame(dct).values

distData = sc.parallelize(dat)

s = distData.map(addToServer).collect()

print(s)

