from keras.preprocessing.image import ImageDataGenerator, img_to_array
from keras.models import load_model
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import cv2
import numpy as np
from PIL import Image
'''In summary, this is the directory structure:
```
dataset-original/
    train/
        metal/
            metal0.jpg
            metal1.jpg
            ...
        paper/
            paper0.jpg
            paper1.jpg
            ...
    validation/
        metal/
            metal0.jpg
            metal1.jpg
            ...
        paper/
            paper0.jpg
            paper1.jpg
            ...
'''

# dimensions of our images.
img_width, img_height = 150, 150

train_data_dir = '/home/user/dataset-original/train'
validation_data_dir = '/home/user/dataset-original/validation'
nb_train_samples = 1895
nb_validation_samples = 500
epochs = 50
batch_size = 16

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(5))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    	rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

model.save_weights('first_try.h5')

#this will give you the label map, that is which numerical value is associated with which class. For eg - [0] maybe associated
#metal, [1] maybe associated with plastic and so on. 
label_map = (train_generator.class_indices)
print(label_map)

#This is the prediction part
im = Image.open('image.jpg')
imrs = im.resize((150,150))
imrs=img_to_array(imrs)/255;
imrs=imrs.reshape(150,150,3);

x=[]
x.append(imrs)
x=np.array(x);

predictions = model.predict(x)
print(predictions)
t = np.argmax(predictions)
print(t)
