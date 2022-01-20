FROM public.ecr.aws/lambda/python:3.8

RUN pip install keras_image_helper
RUN pip install \
    https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.7.0-cp38-cp38-linux_x86_64.whl

COPY lambda.py .
COPY xception_v1_2022-01-16_16_30.tflite .


CMD ["lambda.lambda_handler"]