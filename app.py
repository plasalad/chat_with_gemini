import streamlit as st
import google.generativeai as genai
import pandas as pd

st.set_page_config(page_title="Chat with Database using Gemini", layout="wide")

# Use ONE title
st.title("Chat with Database using Gemini")

# === Sidebar Upload Boxes ===
with st.sidebar:
    st.header("Data File Upload")

    # Upload 1: Transaction CSV
    transaction_file = st.file_uploader(
        "Upload : Transaction file (.csv)",
        type="csv",
        key="transaction_csv"
    )

    # Upload 2: Data Dictionary CSV
    dictionary_file = st.file_uploader(
        "Upload : Data Dictionary (.csv) (if any)",
        type="csv",
        key="dictionary_csv"
    )

# === Main Area ===
if transaction_file:
    st.success("✅ Transaction file uploaded!")
    try:
        transaction_df = pd.read_csv(transaction_file)
        st.subheader("📄 Preview: Transaction Data")
        st.dataframe(transaction_df.head())
    except Exception as e:
        st.error(f"❌ Failed to read transaction CSV: {e}")

if dictionary_file:
    st.success("✅ Data dictionary file uploaded!")
    try:
        dictionary_df = pd.read_csv(dictionary_file)
        st.subheader("📄 Preview: Data Dictionary")
        st.dataframe(dictionary_df.head())
    except Exception as e:
        st.error(f"❌ Failed to read dictionary CSV: {e}")


try:
    # Get Gemini API key from secrets
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)

    # Initialize model
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    # Start chat session if not already in session state
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])


    # Helper to map Gemini roles to Streamlit roles
    def role_to_streamlit(role: str) -> str:
        return 'assistant' if role == 'model' else role

    # Display chat history
    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Chat input
    if prompt := st.chat_input("Text Here"):
        # Show user's message
        st.chat_message('user').markdown(prompt)

        # Send to Gemini and show response
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message('assistant'):
            st.markdown(response.text)

except Exception as e:
    st.error(f'An error occurred: {e}')
