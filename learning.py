from keras.models import Sequential
from keras.layers import Dense,Dropout, Activation, Flatten
from keras.utils import to_categorical
from keras.losses import categorical_crossentropy
from keras.optimizers import SGD


import numpy as np
import pickle
from minio import Minio
from minio.error import ResponseError
from elasticsearch import Elasticsearch

def getFromServer(obj):
	minioClient = Minio('0.0.0.0:9001',access_key='minio',secret_key='minio123',secure=False)
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

data = []
label = []

print(res["hits"]["hits"])

for obj in res["hits"]["hits"]:
	couple = getFromServer(obj)
	data.append(couple[0])
	label.append(couple[1])

data = np.array(data)
label = np.array(label)

model = Sequential()

model.add(Dense(32, input_shape=(32,32,3)))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(5))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

model.fit(data, label, epochs=5, batch_size=32)


scores = model.evaluate(data[:5], label[:5], verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
