from tensorflow.keras.layers import Activation, Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the model
model = Sequential([
    Conv2D(32, (3, 3), input_shape=(image_height, image_width, 1)),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    Conv2D(64, (3, 3)),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    Flatten(),
    Dense(64),
    Activation('relu'),
    
    Dense(1),
    Activation('sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Summary of the model
model.summary()


# Define paths to training data
train_data_dir = 'path_to_dataset_directory'

# Rescale the images by dividing every pixel in every image by 255
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2) # 20% of the data will be used for validation

# Automatically retrieve images and their classes for train and validation sets
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(image_height, image_width),
    batch_size=32,
    color_mode='grayscale',
    class_mode='binary',
    subset='training')

validation_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(image_height, image_width),
    batch_size=32,
    color_mode='grayscale',
    class_mode='binary',
    subset='validation')

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    epochs=10)
