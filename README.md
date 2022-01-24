# Coffee Leaf Rust Predictor

This repository was created as part of the [Machine Learning Bootcamp](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp) by [Alexey Grigorev](https://github.com/alexeygrigorev). This project has been submitted as the final capstone (3rd) project for the course.

I chose this dataset as before working as a software engineer I was a coffee roaster so I have pre existing domain knowledge and a passion for coffee ☕ If you notice any mistakes/ improvements to the code feel free to open an issue 💖

## Identifying Coffee Leaf Rust - the problem we are trying to solve 🕵️‍♀️


[Hemileia vastatrix](https://en.wikipedia.org/wiki/Hemileia_vastatrix) a fungus which causes coffee leaf rust disease. This disease which reduces a plants ability to derive energy through photosynthesis, is extremely damaging to economics built on coffee cultivation as it can wipe out whole crops. The disease can be identified by the spores which cover the plants leaves.

This project focuses on a classification problem, predicting if a image shows a leaf with rust disease or another disease, however with more data it would be interesting to compare healthy leaves and build a multi classifier for all the coffee leaf diseases with images available.

To solve this problem I used the techniques learnt during the course for deep learning. I trained my model using tensorflow using the base model Xception, I tuned several of the parameters to find the most accurate final model. After the final training I converted it to Tensorflow lite so that I could run the model in a lightweight Docker container uploaded to AWS ECR and deployed as a AWS Lambda function. This function can be invoked by calling it at the associated API Gateway. Details for navigating the repository and how it was deployed can be found below :)


## Navigating the project repository 🗂️

Where to find the files for evaluation :)

- 📂 **Analysis**  
    I ran one notebook in Google Colab to do the analysis and model selection so I could leverage the use of a GPU. A copy of it is in the repository [here](analysis/notebooks/leaf_rust_detection_exploration.ipynb).

- 📂 **Scripts**  
    [train.py](./scripts/train.py) runs the training for the final model. [convert.py](./scripts/convert.py) converts the model to a tflite model so it can packaged in a docker container. Predictions are run within a lambda handler, the predict function can be found within the [lambda.py](./src/lambda/lambda.py) file.

- 📂 **Deployment**  
    The lambda function is deployed on [AWS Lambda](https://aws.amazon.com/lambda/) with an [API Gateway](https://aws.amazon.com/api-gateway/) sat in front of it. This end point will remain available until the end of the evaluation period.
    
    
    *Example request to the Lambda Gateway API:*

    ```sh
    curl -X POST https://f7avzh1qu0.execute-api.eu-central-1.amazonaws.com/default/coffee-leaf-rust-prediction?url=https://raw.githubusercontent.com/sleepypioneer/coffee-leaf-rust-predictor/main/src/streamlit_app/static/imgs/1643.jpg

    ```

    *Example response*

    ```
    {"other": "-22.049458", "rust": "5.235355"}
    ```

    The app can be viewed on streamlit [here]]( https://share.streamlit.io/sleepypioneer/coffee-leaf-rust-predictor/main/src/stream_app/main.py).

    You can read more how I went around deploying the above [here](deployment.md).

    I also wrote [deployment.yaml](./src/streamlit_app/deployment.yaml) and [service.yaml](./src/streamlit_app/service.yaml) files for deploying the Streamlit app to Kubernetes, although this is not required for the deployment to the streamlit servers, you could run the following commands inside the `./src/streamlit_app` directory to deploy it and create a service for it:

    ```sh
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```


## Running the project ▶️

### Requirements ⚙️

I advise using a virtual environment for running this project, below are instructions for doing so using [venv](https://docs.python.org/3/library/venv.html) which you can install on linux with the following command `pip install venv`. Additionally if you would like to run the analysis notebooks or the app in Docker you will need to have [Docker](https://docs.docker.com/get-docker/) installed.

### Start a virtual environment 🌐

```sh
# create virtual environment
python3 -m venv venv

# start the virtual environment
source venv/bin/activate

# install virtual environment depencies for linting locally and
# pipenv required for the app's dependency management
pip install -r requirements.txt
```

### Data 💽

The data used for this project is gathered from [Kaggle](https://www.kaggle.com/badasstechie/coffee-leaf-diseases) and has the [CC BY-SA 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/). It consists of 1700+ images of coffee leaves with various diseases. Has annotations and image masks to eliminate backgrounds.

Download this data (including the three CSVs) and put it in to a `./data` directory, subsequent scripts will look for it there.

### Preparing the data

The `data_preparation.py` script will get the datasets ready for training the model on it. You can run it and the clean up with the following make commands (see inside the `.Makefile` to see in more detail the commands that run to do this):

```sh
make prep_data
make clean_up
```

### Training the model and converting a Tensorflow Lite

To run the training script and convert the mdoel to a TFLite model to be used in the lambda service there are two scripts inside `./scripts`: `train.py` and `convert.py` these can be ran together with the make command:

```sh
make prep_model
```

The final model will be saved with a timestamp in its name in the `.models` directory.

### Running the app locally

#### Run the lambda server

To build and run the lambda server I use the following docker commands, for ease I have also put these into Make targets so they can easily be run with one command `make run_lambda_server`.

```sh
cd src/lambda && \
docker build \
    --build-arg model_name=$(MODEL_NAME).tflite \
    -t coffee-leaf-rust-model \
    .


docker run -p 8080:8080 coffee-leaf-rust-model
```

#### Run the streamlit frontend app

Now you have the backend running, inside the virtual environment run the following command to run the streamlit app with live reload on save.

```sh
# This command needs to be run inside the src/app/ directory
# To change into the src/app/ directory
cd src/app
streamlit run --server.runOnSave=True main.py

```

This has also been put behind the Marke target: `make run_app`.

You can now view in your browser the app on the provided local url :D


## Linting your code ✔️
The project is linted with [Black](https://pypi.org/project/black/) and [Flake8](https://pypi.org/project/flake8/) and it is reccomended running these both locally (they are already installed inside the virtual environment following the instructions above) before pushing code as they are enforced in the github actions (see below).

## Github actions 🎬

When pushing code to github it will run actions for linting the code, you can find, add and update these actions in [.github/workflows](./.github/workflows).
