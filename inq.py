# -*- coding: utf-8 -*-
"""INQ.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BbyLPtVbrhW6Om0OoiT8lxTH1uymHAUU
"""

from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)
root_dir = "/content/gdrive/My Drive/"

zip = ZipFile(root_dir+'garbage1/Garbage classification.zip')
zip.extractall(root_dir+'garbage1')

from zipfile import ZipFile
import pandas as pd
import numpy as np
import os
import keras
import matplotlib.pyplot as plt
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam

del model

base_model=MobileNet(weights='imagenet',include_top=False,input_shape=(224,224,3)) #imports the mobilenet model and discards the last 1000 neuron layer.

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(512,activation='relu')(x) #we add dense layers so that the model can learn more complex functions and classify for better results.
x=Dense(512,activation='relu')(x) #dense layer 2
x=Dense(1024,activation='relu')(x) #dense layer 3
preds=Dense(6,activation='softmax')(x) #final layer with softmax activation

model=Model(inputs=base_model.input,outputs=preds)

model.save(root_dir+'garbage1/model1/model.h5')

for layer in model.layers[:20]:
    layer.trainable=False
for layer in model.layers[20:]:
    layer.trainable=True

CLASSES=['cardboard','glass','metal','paper','plastic','trash']
train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) #included in our dependencies

train_generator=train_datagen.flow_from_directory(root_dir+'garbage1/Garbage classification', # this is where you specify the path to the main data folder
                                                 target_size=(224,224),
                                                 color_mode='rgb',
                                                 batch_size=32,
                                                 class_mode='categorical',
                                                 shuffle=True)

model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['categorical_accuracy'])

step_size_train=train_generator.n//train_generator.batch_size
model.fit_generator(generator=train_generator,
                    steps_per_epoch=step_size_train,
                    epochs=20)

model.save_weights(root_dir+'garbage1/weight1/weights.h5')

model.load_weights(root_dir+'garbage1/weight1/weights.h5')

import wget
url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_DctHVvxURANh669qFNZnhQmd3RSPwSwIGTMNUvMS-HBiEeymWQ'
wget.download(url,root_dir+'garbagetest/2.jpg')

from PIL import Image
img=Image.open(root_dir+'garbage1/Garbage classification/plastic/plastic89.jpg')
import matplotlib.pyplot as plt
plt.imshow(img)
img=img.resize((224,224))

img=np.array(img)
p=model.predict(preprocess_input(img.reshape(1,224,224,3)))
CLASSES[np.argmax(p)]

CLASSES

model.save(root_dir+'garbage1/model1/model.h5')

import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_keras_model_file(root_dir+"garbage1/model1/model.h5")
tflite_model = converter.convert()
open(root_dir+"garbage1/model1/converted_model.tflite", "wb").write(tflite_model)

3