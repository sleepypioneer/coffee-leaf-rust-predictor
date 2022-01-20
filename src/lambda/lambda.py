import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor

preprocessor = create_preprocessor('xception', target_size=(150, 150))

interpreter = tflite.Interpreter(model_path="./xception_v1_2022-01-16_16_30.tflite")
interpreter.allocate_tensors()


classes = ['other', 'rust']

input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]


def predict(img_url: str, input_size: int=299):
    X = preprocessor.from_path(img_url)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    
    return dict(zip(classes, preds[0]))


def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result