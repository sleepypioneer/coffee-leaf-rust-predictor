import tensorflow as tf
from tensorflow import keras



def convert_to_tf_lite(model_path:str, model_name: str):
    model = keras.models.load_model(model_path)


    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    with open(f"{model_name}.tflite", "wb") as f_out:
        f_out.write(tflite_model)

    print("Model saved as tf lite model")


if __name__ == "__main__":
    MODEL_PATH = "../../models/xception_v1_2022-01-16_16_30.h5"
    MODEL_NAME = "xception_v1_2022-01-16_16_30"

    convert_to_tf_lite(MODEL_PATH, MODEL_NAME)