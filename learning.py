from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten,Conv2D, MaxPooling2D

from pyspark import SparkContext
from pyspark import SparkConf

import numpy as np
import pickle
from elasticsearch import Elasticsearch

import sys

conf = SparkConf()
conf.setMaster("spark://0.0.0.0:7077")
conf.setAppName("NumpyMult")
sc = SparkContext(conf=conf)

def getFromServer(obj):
	from minio import Minio
	from minio.error import ResponseError
	minioClient = Minio('minio:9000',access_key='minio',secret_key='minio123',secure=False)
	ret = 0
	try:
		recv = minioClient.get_object('dat',obj["_source"]['image'])

		image = pickle.loads(recv.read())
		
		label = obj["_source"]['label']

		if label in '[1. 0. 0. 0. 0.]':
			label = np.array([1,0,0,0,0])
		elif label in '[0. 1. 0. 0. 0.]':
			label = np.array([0,1,0,0,0])
		elif label in '[0. 0. 1. 0. 0.]':
			label = np.array([0,0,1,0,0])
		elif label in '[0. 0. 0. 1. 0.]':
			label = np.array([0,0,0,1,0])
		elif label in '[0. 0. 0. 0. 1.]':
			label = np.array([0,0,0,0,1])

		ret = (image,label)
	except:
		ret = (0,0)

	return ret

es = Elasticsearch(['http://0.0.0.0:9200'])

res = es.search(index="images_classification", body={"query": {"match_all": {}}})

size = res["hits"]["total"]

res = es.search(index="images_classification", body={"query": {"match_all": {}}},size=size)

data = []
label = []

distData = sc.parallelize(res["hits"]["hits"])

s = distData.map(getFromServer).collect()

for obj in s:
	data.append(obj[0])
	label.append(obj[1])

data = np.array(data)
label = np.array(label)

model = Sequential()
model.add(Conv2D(256, (3, 3), input_shape=data.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(64))

model.add(Dense(5))
model.add(Activation('softmax'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

model.fit(data, label, epochs=5, batch_size=32)

test_label = np.load(sys.argv[2])
test_data = np.load(sys.argv[1], mmap_mode='r')

scores = model.evaluate(test_data, test_label, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
