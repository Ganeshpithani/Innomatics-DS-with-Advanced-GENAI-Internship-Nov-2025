import streamlit as st
import pickle
import base64
import os

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Flipkart Reviews",
    page_icon="🛒", # Changed to emoji for better compatibility
    layout="centered"
)

# ------------------ Background Image Function ------------------
def set_background(image_file):
    # This ensures the script looks in the same folder as the app.py file
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, image_file)
    
    try:
        with open(full_path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"❌ Background image not found at {full_path}. Please check the filename.")

# Set background (Double check this spelling!)
set_background("flipkartimge.jpg")

# ------------------ Load Model ------------------
@st.cache_resource
def load_model():
    # Adding path resolution here too for safety
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, "flipkart_sm.pkl")
    
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    return model

# Only load model if it exists to avoid crashing
if os.path.exists(os.path.join(os.path.dirname(__file__), "flipkart_sm.pkl")):
    model = load_model()
else:
    st.error("❌ Model file 'flipkart_sm.pkl' not found!")
    st.stop()

# ------------------ UI ------------------
st.markdown(
    "<h1 style='color:white;'>Flipkart Reviews Classification</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:white;'>Predict the category using flipkart review classification </p>",
    unsafe_allow_html=True
)

user_input = st.text_area(
    "Enter Review",
    placeholder="Good Quality product..."
)

if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        # Some models require vectorization before prediction. 
        # If your 'model' is a Pipeline, this works as is.
        prediction = model.predict([user_input])[0]
        st.success(f"🎯 Predicted Category: **{prediction}**")