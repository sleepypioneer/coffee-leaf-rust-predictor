from datetime import datetime
import pathlib
from typing import Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import load_img

batch_size = 32
img_height = 150
img_width = 150
input_shape=(150, 150, 3)

train_data_path = "./coffee-leaf-diseases/coffee-leaf-diseases/train/images/"
data_dir = pathlib.Path(train_data_path)


def make_model(input_size=150, learning_rate=0.01, size_inner=100,
               droprate=0.5):

    base_model = Xception(
        weights='imagenet',
        include_top=False,
        input_shape=(input_size, input_size, 3)
    )

    base_model.trainable = False

    #########################################

    inputs = keras.Input(shape=(input_size, input_size, 3))
    base = base_model(inputs, training=False)
    vectors = keras.layers.GlobalAveragePooling2D()(base)
    
    inner = keras.layers.Dense(size_inner, activation='relu')(vectors)
    drop = keras.layers.Dropout(droprate)(inner)
    
    outputs = keras.layers.Dense(2)(drop)
    
    model = keras.Model(inputs, outputs)
    
    #########################################

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    loss = keras.losses.CategoricalCrossentropy(from_logits=True)

    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=['accuracy']
    )
    
    return model


def generate_train_val_ds(data_dir: str) -> Any:
    train_gen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        zoom_range=0.1,
        horizontal_flip=True,
        validation_split=0.2
    )

    train_ds = train_gen.flow_from_directory(
        data_dir,
        subset="training",
        target_size=(input_size, input_size),
        batch_size=32
    )

    val_ds = train_gen.flow_from_directory(
        data_dir,
        subset="validation",
        target_size=(input_size, input_size),
        batch_size=32,
        shuffle=False
    )

    return train_ds, val_ds


def convert_to_tf_lite(final_model):
    converter = tf.lite.TFLiteConverter.from_keras_model(final_model)
    return converter.convert()


if __name__ == "__main__":
    input_size=299

    final_model = make_model(
        input_size=input_size,
        learning_rate=0.2,
        size_inner=100,
        droprate=0.2
    )

    train_ds, val_ds = generate_train_val_ds(data_dir)

    final_model.fit(train_ds, epochs=10, validation_data=val_ds)

    tflite_model = convert_to_tf_lite(final_model)

    version = "1"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H:%M")
    model_name = f"xception_v{version}_{timestamp}"

    final_model.save(f"{model_name}.h5")
    print("Model saved")

    with open(f"data/{model_name}.tflite", "wb") as f_out:
        f_out.write(tflite_model)
    
    print("Model saved as tf lite model")