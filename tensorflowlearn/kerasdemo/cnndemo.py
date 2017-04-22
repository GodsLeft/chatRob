# coding:utf-8
import numpy as np
np.random.seed(1337)
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, Flatten, MaxPooling2D
from keras.optimizers import Adam

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 1, 28, 28)
X_test = X_test.reshape(-1, 1, 28, 28)
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# build cnn model
model = Sequential()

# conv1
model.add(Convolution2D(
    nb_filter=32,
    kernel_size=[5,5],
    border_mode='same',
    input_shape = (1, 28, 28),
))
model.add(Activation('relu'))

# pooling1
model.add(MaxPooling2D(
    pool_size=(2, 2),
    strides=(2, 2),
    border_mode='same',
))

# conv2
model.add(Convolution2D(64, 25, border_mode='same'))
model.add(Activation('relu'))

# max pooling2
model.add(MaxPooling2D(pool_size=(2, 2), border_mode='same'))

# 全连阶层
model.add(Flatten())
model.add(Dense(1024))
model.add(Activation('relu'))

# 第二个全连阶层
model.add(Dense(10))
model.add(Activation('softmax'))

# define optimizer
adam = Adam(lr=1e-4)

model.compile(optimizer=adam,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print('Training ----------')
model.fit(X_train, y_train, nb_epoch=1, batch_size=32)

print('Testing -----------')
loss, accuracy = model.evaluate(X_test, y_test)

print('test loss: ', loss)
print('test accu: ', accuracy)