import streamlit as st

from chat import display_chat_interface

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

st.set_page_config(
    page_title="Ruvunga's Chatbot",

)

st.title("Ruvunga's ChatBot 🏭")

display_chat_interface()