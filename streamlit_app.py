import streamlit as st
import requests
import io

# Define FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Streamlit Page Config
st.set_page_config(page_title="GenAI App", page_icon="🤖", layout="wide")

# App Title
st.title("📄 Generative AI Document Processing & Chatbot")

# Upload Document Section
st.header("📤 Upload a Document")

uploaded_file = st.file_uploader("Upload your document", type=["txt", "pdf", "docx"])
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, io.BytesIO(uploaded_file.getvalue()))}
    try:
        with st.spinner("Uploading and processing..."):
            response = requests.post(f"{FASTAPI_URL}/upload/", files=files)
        response.raise_for_status()
        st.success("✅ Document uploaded and processed successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Server error: {e}")

# Generate Insights Section
st.header("📊 Generate Insights")
if st.button("Generate Insights"):
    try:
        with st.spinner("Generating insights..."):
            response = requests.get(f"{FASTAPI_URL}/insights/")
        response.raise_for_status()
        insights = response.json()["insights"]
        st.success("✅ Insights generated successfully!")
        st.write(insights)
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Server error: {e}")

# Chatbot Section
st.header("💬 Chat with AI")
query = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if not query:
        st.warning("⚠️ Please enter a query.")
    else:
        try:
            with st.spinner("Fetching response..."):
                response = requests.post(f"{FASTAPI_URL}/chat/", json={"query": query})
            response.raise_for_status()
            reply = response.json()["response"]
            st.success("✅ AI Response:")
            st.write(reply)
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Server error: {e}")