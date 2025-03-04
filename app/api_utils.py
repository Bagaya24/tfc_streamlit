import requests
import streamlit as st

def get_api_response(question: str, session_id: str | None):
    try:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "question": question,
        }
        if session_id:
            data["session_id"] = session_id
        response = requests.post("http://127.0.0.1:8000/chat", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()

        else:
            st.error(f"La requête vers l'api a echoué, error: {response.status_code}-{response.text}")
            return None
    except Exception as e:
        st.error(f"Il semble y avoir une erreur avec le systeme, error: {str(e)}")
        return None

