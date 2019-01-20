import numpy as np
import pickle
from minio import Minio
from minio.error import ResponseError
from pyspark import SparkContext
from pyspark import SparkConf
from elasticsearch import Elasticsearch

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import SGD
from keras.losses import categorical_crossentropy
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

es = Elasticsearch(['http://elasticsearch:9200'])

res = es.search(index="images_classification", body={"query": {"match_all": {}}},size=1222)

distData = sc.parallelize(res["hits"]["hits"])

s = distData.map(getFromServer).collect()

data = []
label = []

for couple in s:
	data.append(couple[0])
	label.append(couple[1])

data = np.array(data)
label = np.array(label)

print(data.shape)

model = Sequential()

model.add(Dense(32, input_shape=(32,32,3)))

model.add(Flatten())
model.add(Dense(256, activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(5, activation = "softmax"))

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])


rdd = to_simple_rdd(sc, data, label)


spark_model = SparkModel(model, frequency='epoch', mode='asynchronous')


spark_model.fit(rdd, epochs=2, batch_size=32, verbose=0, validation_split=0.1)


score, acc = spark_model.evaluate(data[:10], label[:10], show_accuracy=True, verbose=0)
print('Test accuracy:', acc)
