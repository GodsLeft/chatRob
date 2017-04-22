# coding:utf-8
import numpy as np
np.random.seed(1337)
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import SimpleRNN, Activation, Dense
from keras.optimizers import Adam

# 一行一行的读取整张图片，读完一张图片之后，总结
TIME_STEPS = 28  # 一个时间点，28行数据
INPUT_SIZE = 28
BATCH_SIZE = 50
BATCH_INDEX = 0
OUTPUT_SIZE = 10
CELL_SIZE = 50  # 50个神经元
LR = 0.001

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(-1, 28, 28) / 255
X_test = X_test.reshape(-1, 28, 28) / 255
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# build RNN model
model = Sequential()

model.add(SimpleRNN(
    batch_input_shape=[BATCH_SIZE, TIME_STEPS, INPUT_SIZE],
    output_dim=CELL_SIZE,
))

model.add(Dense(OUTPUT_SIZE))
model.add(Activation('softmax'))

adam = Adam(LR)
model.compile(optimizer=adam,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# training
for step in range(4001):
    X_batch = X_train[BATCH_INDEX: BATCH_SIZE + BATCH_INDEX, :, :]
    Y_batch = y_train[BATCH_INDEX: BATCH_SIZE + BATCH_INDEX, :]
    cost = model.train_on_batch(X_batch, Y_batch)
    BATCH_INDEX += BATCH_SIZE
    BATCH_INDEX = 0 if BATCH_INDEX >= X_train.shape[0] else BATCH_INDEX

    if step % 500 == 0:
        cost, accuracy = model.evaluate(X_test, y_test, batch_size=y_test.shape[0], verbose=False)
        print('test cost: ', cost, 'test accuracy: ', accuracy)