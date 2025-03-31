from tensorflow.keras.models import load_model
import streamlit as st
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

labels = {1:"Bud Root Dropping", 2:"Bud Rot", 3:"Gray Leaf Spot", 4:"Leaf Rot", 5:"Stem Bleeding"}

model = load_model(r"D:\Data Science\Coconut Tree Disease Data - Copy\CoconutDisease.h5")

def processed_img(img_path):
    img = load_img(img_path, target_size=(256, 256, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = int(y_class[0])
    res = labels[y]
    print(res)
    return res.capitalize()

def run():
    st.title("Coconut Disease Classifia")
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, use_column_width=False)
        save_image_path = "D:/Data Science/Coconut Tree Disease Data - Copy//upload_images/" + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result = processed_img(save_image_path)
            print(result)
            st.info('**Category : Vegetables**')


run()
