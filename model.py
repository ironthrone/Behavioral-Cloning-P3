import csv
import cv2
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import random
import skimage.transform as transform
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Conv2D, \
    MaxPooling2D, Activation, Cropping2D, Dropout
from keras.optimizers import SGD, Adam

def generator(lines, batch=20):
    '''
    generator,it receive row list ,return a tuple of datas and labels
    '''
    samples_length = len(lines)
    while True:
        for i in range(0, samples_length, batch):
            batch_lines = lines[i:i + batch]
            data = []
            target = []
            for line in batch_lines:
                img = cv2.imread(line[0])
                steering = float(line[3])
                data.append(img)
                target.append(steering)

                # add correct img to teach car go back to center of road
                left_img = cv2.imread(line[1])
                left_img_steering = steering + 0.1
                right_img = cv2.imread(line[2])
                right_img_steering = steering - 0.1

                data.append(left_img)
                target.append(left_img_steering)
                data.append(right_img)
                target.append(right_img_steering)

                # add mirror img to teach car switch right
                mirror_img = np.fliplr(img)
                mirror_steering = -steering
                data.append(mirror_img)
                target.append(mirror_steering)

                # add random rotated image
                rotated = transform.rotate(img, angle=random.randint(-15, 15), preserve_range=True)
                data.append(rotated)
                target.append(steering)
            # print('batch data size is %d' % len(data))
            yield (np.array(data), np.array(target))

lines = []
with open('./record/driving_log.csv') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        # every second 10 frame
        if index % 20 < 10:
            lines.append(row)


lines = shuffle(lines)
train_validation_set, test_set = train_test_split(lines, test_size=0.2)
train_set, validation_set = train_test_split(train_validation_set, test_size=0.2)

batch_size = 10  # with imrror,left and right camera data,the actual batch size is 40
train_generator = generator(train_set, batch_size)
validation_generator = generator(validation_set, batch_size)

# test data
test_X = []
test_y = []
for line in test_set:
    test_X.append(cv2.imread(line[0]))
    test_y.append(line[3])
test_X = np.array(test_X)
test_y = np.array(test_y)

# create a  model,and train it
print('Construct model')


model = Sequential()

model.add(Lambda(lambda x: x / 127.5 - 1, input_shape=(160, 320, 3)))
model.add(Cropping2D(cropping=((50, 20), (0, 0))))  # crop the img
print(model.output.shape)
model.add(Conv2D(kernel_size=(5, 5), strides=(1, 1), filters=24, padding='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(kernel_size=(5, 5), strides=(1, 1), filters=36, padding='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(kernel_size=(5, 5), strides=(1, 1), filters=48, padding='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(kernel_size=(3, 3), strides=(1, 1), filters=64, padding='valid'))
model.add(Activation('relu'))

model.add(Conv2D(kernel_size=(3, 3), strides=(1, 1), filters=64, padding='valid'))
model.add(Activation('relu'))

model.add(Flatten())
model.add(Dense(units=400))
model.add(Activation('relu'))
model.add(Dropout(0.35))
model.add(Dense(units=50))
model.add(Activation('relu'))
model.add(Dropout(0.35))
model.add(Dense(units=10))
model.add(Activation('relu'))
model.add(Dropout(0.35))
model.add(Dense(1))

# original Lenet model
# model.add(Conv2D(kernel_size=(5,5),strides=(1,1),filters=24,padding='valid'))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
# model.add(Conv2D(kernel_size=(5,5),strides=(1,1),filters=36,padding='valid'))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
#
# model.add(Flatten())
# model.add(Dense(units=120))
# model.add(Activation('relu'))
# model.add(Dropout(0.35))
# model.add(Dense(units=84))
# model.add(Activation('relu'))
# model.add(Dropout(0.35))
# model.add(Dense(1))


adam = Adam(lr=0.0005)
model.compile(optimizer=adam, loss='mse')

print("Start training...")
train_history = model.fit_generator(generator=train_generator,
                                    validation_data=validation_generator,
                                    steps_per_epoch=4 * len(train_set) // batch_size,
                                    verbose=2,
                                    validation_steps=4 * len(validation_set) // batch_size, epochs=10)

# test on test data
test_error = model.evaluate(test_X, test_y, batch_size=50, verbose=2)
print('Test error is {}'.format(test_error))

# save model architecture and weights
model.summary()
model.save('model.h5')


# plot the loss along epoch
plt.figure()
plt.plot(train_history.history['loss'])
plt.plot(train_history.history['val_loss'])
plt.xlabel('epoch of train')
plt.ylabel('mean squared loss')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.savefig('test.png')
