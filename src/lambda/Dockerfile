FROM public.ecr.aws/lambda/python:3.8

RUN pip install keras_image_helper
RUN pip install \
    https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.7.0-cp38-cp38-linux_x86_64.whl

ARG model_name
ENV MODEL_NAME=$model_name

COPY lambda.py .
COPY $MODEL_NAME .

CMD ["lambda.lambda_handler"]