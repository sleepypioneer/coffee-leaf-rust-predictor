import typer

import tensorflow as tf
from tensorflow import keras


def convert_to_tf_lite(model_path: str, model_name: str):
    model = keras.models.load_model(model_path)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    return converter.convert()


def main(
    model_name: str = typer.Option(...),
    models_path: str = "./models",
):
    MODEL_PATH = f"{models_path}/{model_name}.h5"

    tflite_model = convert_to_tf_lite(MODEL_PATH, model_name)

    with open(f"{models_path}/{model_name}.tflite", "wb") as f_out:
        f_out.write(tflite_model)

    print("Model saved as tf lite model")


if __name__ == "__main__":
    typer.run(main)
