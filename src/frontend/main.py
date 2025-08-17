import streamlit as st
import requests

st.set_page_config(
    page_title="PolicyRAG - Budget 2025 Assistant",
    layout="centered",
)

st.title("💰 PolicyRAG - Budget 2025 Assistant")
st.markdown("Ask any question about the Union Budget 2025 and get clear, source-backed answers.")

api_url = "https://policyrag.onrender.com/query"

def get_answer(question_text):
    try:
        payload = {"question": question_text}
        response = requests.post(api_url, json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            return data.get("answer", "Sorry, I couldn't find an answer.")
        else:
            return f"API Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents and generating an answer..."):
            answer = get_answer(prompt)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})