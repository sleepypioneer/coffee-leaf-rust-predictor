import os
from typing import Any
import typer

from PIL import Image
import requests
import streamlit as st

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
ENV = os.getenv("ENV")
LAMBDA_URL = os.getenv("LAMBDA_URL") if ENV == "dev" else st.secrets["LAMBDA_URL"]


def fetch_predictions(img_url: str) -> Any:
    print("fetching predictions....")
    if ENV == "dev":
        # the dev local version takes the url from the body
        data = {"url": img_url}
        resp = requests.post(LAMBDA_URL, json=data)
    else:
        # the prod API gateway extracts the url from the param
        resp = requests.post(f"{LAMBDA_URL}?url={img_url}")
    print(resp)
    if resp.status_code != 200:
        return "No prediction given"
    return resp.json()


def predict(img_url: str) -> str:
    result = fetch_predictions(img_url)
    print(result)
    other = float(result["other"])
    rust = float(result["rust"])

    print(other, rust)
    if other > rust:
        return "other"
    else:
        return "rust"


def app() -> None:
    # Title and info
    st.title("Coffee Leaf Rust Identifier:")

    st.info(
        """
        Hemileia vastatrix a fungus which causes coffee leaf rust disease.
        This disease which reduces a plants ability to derive energy through
        photosynthesis, it is extremely damaging to economics built on coffee
        cultivation as it can wipe out whole crops.
        The disease can be identified by the spores which cover the plants leaves.
        \n\n
        I trained a model on a dataset of images of coffee leaves with different diseases
        to predict if the image contained a leaf with Coffee rust disease or not
        (it may have a different disease present).
        \n\n
        To demonstrate the model you can chose one of the images of leaves below and
        click it's corresponding button to get a prediction for it.
        """
    )

    img_1_path = os.path.join(CURR_DIR, "static/imgs/1.jpg")
    image_1 = Image.open(img_1_path)
    st.image(image_1, caption="coffee leaf", use_column_width=True)

    # Run predictions
    if st.button("Predict if this leaf has rust"):
        prediction = predict(
            "https://raw.githubusercontent.com/sleepypioneer/coffee-leaf-rust-predictor/main/src/app/static/imgs/1.jpg"  # noqa
        )
        st.title(f"Prediction: {prediction}")

    img_2_path = os.path.join(CURR_DIR, "static/imgs/1643.jpg")
    image_2 = Image.open(img_2_path)
    st.image(image_2, caption="coffee leaf", use_column_width=True)

    # Run predictions
    if st.button("Predict if the leaf has rust"):
        prediction = predict(
            "https://raw.githubusercontent.com/sleepypioneer/coffee-leaf-rust-predictor/main/src/app/static/imgs/1643.jpg"  # noqa
        )
        st.title(f"Prediction: {prediction}")


if __name__ == "__main__":
    # Need to do this try/except due to Streamlit weirdness
    # See https://github.com/streamlit/streamlit/issues/468
    try:
        typer.run(app)
    except SystemExit as e:
        if e.code != 0:
            raise
