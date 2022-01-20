from PIL import Image
import requests
import streamlit as st
import typer
import os

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
LAMBDA_URL = 'http://localhost:8080/2015-03-31/functions/function/invocations'


def fetch_predictions(img_url: str)-> str:
    print("fetching predictions....")
    data = {"url": img_url}
    resp = requests.post(LAMBDA_URL, json=data)
    print(resp)
    
    json_resp = resp.json()
    print(json_resp)
    return json_resp
    

def app() -> None:
    # Title and info
    st.title('Coffee Leaf Rust Identifier:')

    st.info(
        """
        Hemileia vastatrix a fungus which causes coffee leaf rust disease.
        This disease which reduces a plants ability to derive energy through photosynthesis, is extremely damaging to 
        economics built on coffee cultivation as it can wipe out whole crops. 
        The disease can be identified by the spores which cover the plants leaves.
        \n\n
        I trained a model on a dataset of images of coffee leaves with different diseases to predict if the image contained a
        leaf with Coffee rust disease or not (it may have a different disease present).
        \n\n
        To demonstrate the model you can chose one of the images of leaves below and click it's corresponding button to get a prediction for it.
        """)
    
    
    
    img_1_path = os.path.join(CURR_DIR, 'static/imgs/514.jpg')
    image_1 = Image.open(img_1_path)
    st.image(image_1, caption="coffee leaf", use_column_width=True)

    # Run predictions
    if st.button("Predict if this leaf has rust"):
        prediction = fetch_predictions(img_1_path)
        survival = 'Other disease'
        if prediction == [1]:
            survival = 'Rust'
        st.title(f'Prediction: {survival}')

    img_2_path = os.path.join(CURR_DIR, 'static/imgs/1643.jpg')
    image_2 = Image.open(img_2_path)
    st.image(image_2, caption="coffee leaf", use_column_width=True)

    # Run predictions
    if st.button("Predict if the leaf has rust"):
        prediction = fetch_predictions(img_2_path)
        st.title(f'Prediction: {prediction}')


if __name__ == "__main__":
    # Need to do this try/except due to Streamlit weirdness
    # See https://github.com/streamlit/streamlit/issues/468
    try:
        typer.run(app)
    except SystemExit as e:
        if e.code != 0:
            raise