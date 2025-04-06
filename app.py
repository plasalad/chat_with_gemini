import streamlit as st
import google.generativeai as genai

try:
    # Get Gemini API key from secrets
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)

    # Initialize model
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    # Start chat session if not already in session state
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    # Page title
    st.title('Gemini Pro Test')

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
