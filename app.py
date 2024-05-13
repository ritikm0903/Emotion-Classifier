from multiapp import Multiapp
from pages import home, text, speech, emotionClassifier  # Import the new module
import streamlit as st

# Set the port
# st.set_option('server.port', 8502)

app = Multiapp()

app.add_app("Home", home.app)
app.add_app("Emotion Text Classifier", emotionClassifier.app)
# app.add_app("Text to speech", text.app)   

app.run()
