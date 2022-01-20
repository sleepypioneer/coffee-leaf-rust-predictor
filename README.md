# Coffee Leaf Rust Predictor

This repository was created as part of the [Machine Learning Bootcamp](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp) by [Alexey Grigorev](https://github.com/alexeygrigorev). This project has been submitted as the midterm project for the course.

I chose this dataset as before working as a software engineer I was a coffee roaster so I have pre existing domain knowledge and a passion for coffee ☕ If you notice any mistakes/ improvements to the code feel free to open an issue 💖

## Identifying Coffee Leaf Rust - the problem we are trying to solve 🕵️‍♀️


[Hemileia vastatrix](https://en.wikipedia.org/wiki/Hemileia_vastatrix) a fungus which causes coffee leaf rust disease. This disease which reduces a plants ability to derive energy through photosynthesis, is extremely damaging to economics built on coffee cultivation as it can wipe out whole crops. The disease can be identified by the spores which cover the plants leaves.

This project focuses on a classification problem, predicting if a image shows a leaf with rust disease or another disease, however with more data it would be interesting to compare healthy leaves and build a multi classifier for all the coffee leaf diseases with images available.

## Navigating the project repository 🗂️

Where to find the files for evaluation :)

- 📂 **Analysis**
    I ran one notebook in Google Colab to do the analysis and model selection so I could leverage the use of a GPU. A copy of it is in the repository [here](analysis/notebooks/leaf_rust_detection_exploration.ipynb).

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

### Running the app locally

#### Run the lambda server

First build the model image and lambda image sequentially

```sh
docker build \
    -f ./src/lambda/Dockerfile \
    -t coffee-leaf-rust-model \
    .
```

Next run the lambda container so it can be accessed locally.

```sh
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

You can now view in your browser the app on the provided local url :D

## Data 💽

The data used for this project is gathered from [Kaggle](https://www.kaggle.com/badasstechie/coffee-leaf-diseases) and has the [CC BY-SA 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/). It consists of 1700+ images of coffee leaves with various diseases. Has annotations and image masks to eliminate backgrounds.

## Linting your code ✔️
The project is linted with [Black](https://pypi.org/project/black/) and [Flake8](https://pypi.org/project/flake8/) and it is reccomended running these both locally (they are already installed inside the virtual environment following the instructions above) before pushing code as they are enforced in the github actions (see below).

## Github actions 🎬

When pushing code to github it will run actions for linting the code, you can find, add and update these actions in [.github/workflows](./.github/workflows).