from datetime import datetime
import pathlib
from typing import Any, Tuple
import typer

from tensorflow import keras

from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def make_model(input_size=150, learning_rate=0.01, size_inner=100, droprate=0.5):

    base_model = Xception(
        weights="imagenet", include_top=False, input_shape=(input_size, input_size, 3)
    )

    base_model.trainable = False

    #########################################

    inputs = keras.Input(shape=(input_size, input_size, 3))
    base = base_model(inputs, training=False)
    vectors = keras.layers.GlobalAveragePooling2D()(base)

    inner = keras.layers.Dense(size_inner, activation="relu")(vectors)
    drop = keras.layers.Dropout(droprate)(inner)

    outputs = keras.layers.Dense(2)(drop)

    model = keras.Model(inputs, outputs)

    #########################################

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    loss = keras.losses.CategoricalCrossentropy(from_logits=True)

    model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy"])

    return model


def generate_train_val_ds(data_dir: str, input_size: int = 299) -> Any:
    train_gen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        zoom_range=0.1,
        horizontal_flip=True,
        validation_split=0.2,
    )

    train_ds = train_gen.flow_from_directory(
        data_dir, subset="training", target_size=(input_size, input_size), batch_size=32
    )

    val_ds = train_gen.flow_from_directory(
        data_dir,
        subset="validation",
        target_size=(input_size, input_size),
        batch_size=32,
        shuffle=False,
    )

    return train_ds, val_ds


def main(
    model_name: str = typer.Option(...),
    train_data_path: str = typer.Option(...),
    output_path: str = "./models",
    input_size: int = 299,
):
    data_dir = pathlib.Path(train_data_path)

    final_model = make_model(input_size=input_size, learning_rate=0.2, size_inner=100, droprate=0.2)

    train_ds, val_ds = generate_train_val_ds(data_dir)

    final_model.fit(train_ds, epochs=10, validation_data=val_ds)

    model_path = f"{output_path}/{model_name}.h5"
    final_model.save(model_path)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    typer.run(main)
