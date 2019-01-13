import numpy as np
from minio import Minio
from minio.error import ResponseError
import time
from pyspark import SparkContext
from pyspark import SparkConf
from tempfile import NamedTemporaryFile
 
conf = SparkConf()
conf.setMaster("spark://master:7077")
conf.setAppName("NumpyMult")
sc = SparkContext(conf=conf)


def addToServer(image):
	minioClient = Minio('minio:9000',access_key='minio',secret_key='minio123',secure=False)
	ret = 0
	try:
		tempfile = NamedTemporaryFile()
		np.save(tempfile, image)
		tempfile.seek(0)

		if not minioClient.bucket_exists('datas'):
			minioClient.make_bucket('datas')

		minioClient.fput_object('datas', str(time.time())+".npy", tempfile.name)
		ret = time.time()
	except:
		ret = 0

	return ret

data = np.load('/home/train.npy')
distData = sc.parallelize(data)

s = distData.map(addToServer).collect()

print(s)

