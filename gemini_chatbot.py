import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Set up the Streamlit app
st.set_page_config(page_title="Multimodal Chatbot with Gemini Flash", layout="wide")
st.title("Multimodal Chatbot with Gemini Flash")
st.caption("Chat with Google's Gemini Flash model using image and text input to get lightning-fast results")

# Get the Google API key from the user
api_key = st.text_input("Enter Google API key", type="password")

# Setup the Gemini model
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

    # Initialize the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for image upload
    with st.sidebar:
        st.title("Chat with Images")
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

    # Main layout
    chat_placeholder = st.container()

    with chat_placeholder:
        # Display the chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input area at the bottom
    prompt = st.chat_input("What do you want to know?")

    if prompt:
        inputs = [prompt]

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with chat_placeholder:
            with st.chat_message("user"):
                st.markdown(prompt)

            if uploaded_file:
                inputs.append(image)

            with st.spinner("Generating response..."):
                # Generate response
                response = model.generate_content(inputs)

            # Display assistant response in chat message container
            with chat_placeholder:
                with st.chat_message("assistant"):
                    st.markdown(response.text)

            if uploaded_file and not prompt:
                st.warning("Please enter a text query to accompany the chat image.")
else:
    st.warning("Please enter your Google API key to proceed.")
