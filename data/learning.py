import numpy as np
import pickle
from minio import Minio
from minio.error import ResponseError
from pyspark import SparkContext
from pyspark import SparkConf
from elasticsearch import Elasticsearch

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from elephas.utils.rdd_utils import to_simple_rdd
from elephas.spark_model import SparkModel
 
conf = SparkConf()
conf.setMaster("spark://master:7077")
conf.setAppName("Learning")
sc = SparkContext(conf=conf)


def getFromServer(obj):
	minioClient = Minio('minio:9000',access_key='minio',secret_key='minio123',secure=False)
	ret = 0
	try:
		recv = minioClient.get_object('dat',obj["_source"]['image'])

		image = pickle.loads(recv.read())
		
		label = obj["_source"]['label']

		if label in '[1. 0. 0. 0. 0.]':
			label = 0
		elif label in '[0. 1. 0. 0. 0.]':
			label = 1
		elif label in '[0. 0. 1. 0. 0.]':
			label = 2
		elif label in '[0. 0. 0. 1. 0.]':
			label = 3
		elif label in '[0. 0. 0. 0. 1.]':
			label = 4

		ret = (image,label)
	except:
		ret = (0,0)

	return ret

es = Elasticsearch(['http://elasticsearch:9200'])

res = es.search(index="images_classification", body={"query": {"match_all": {}}})

distData = sc.parallelize(res["hits"]["hits"])

s = distData.map(getFromServer).collect()

data = []
label = []

for couple in s:
	data.append(couple[0])
	label.append(couple[1])

model = Sequential()
model.add(Dense(128, input_dim=784))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(10))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer=SGD())

print("11111111111111111111111111111111")

rdd = to_simple_rdd(sc, data, label)

print("2222222222222222222222222")

spark_model = SparkModel(model, frequency='epoch', mode='asynchronous')

print("555555555555555555555555555")

spark_model.fit(rdd, epochs=20, batch_size=32, verbose=0, validation_split=0.1)

print("66666666666666666666666666")

score, acc = spark_model.evaluate(data[:10], label[:10], show_accuracy=True, verbose=0)
print('Test accuracy:', acc)
