FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

ARG lambda_url
ENV LAMBDA_URL=$lambda_url

COPY ./static ./
COPY main.py ./

CMD ["streamlit", "run", "--server.runOnSave=True", "main.py"]