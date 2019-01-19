import numpy as np
from minio import Minio
from minio.error import ResponseError
from pyspark import SparkContext
from pyspark import SparkConf
from elasticsearch import Elasticsearch
 
conf = SparkConf()
conf.setMaster("spark://master:7077")
conf.setAppName("NumpyMult")
sc = SparkContext(conf=conf)


def getFromServer(obj):
	minioClient = Minio('minio:9000',access_key='minio',secret_key='minio123',secure=False)
	ret = 0
	try:
		recv = minioClient.get_object('dat',obj["_source"]['image'])

		image = np.frombuffer(recv.read(), dtype='int')
		
		label = obj["_source"]['label']

		ret = (image,label)
	except:
		ret = (0,0)

	return ret

es = Elasticsearch(['http://elasticsearch:9200'])

res = es.search(index="images_classification", body={"query": {"match_all": {}}})

distData = sc.parallelize(res["hits"]["hits"])

s = distData.map(getFromServer).collect()

print(s)

