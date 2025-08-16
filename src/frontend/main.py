import streamlit as st
import requests

st.set_page_config(
    page_title="PolicyRAG - Budget 2025 Assistant",
    page_icon="💰",
    layout="centered",
)

st.title("💰 PolicyRAG - Budget 2025 Assistant")
st.markdown(
    "Ask any question about Budget 2025 and get concise answers from our assistant."
)

api_url = "http://localhost:8000/query"

question = st.text_input("Type your question here:")

def get_answer(question_text):
    try:
        payload = {"question": question_text}
        response = requests.post(api_url, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "Sorry, I couldn't find an answer.")
            return answer
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

if st.button("Get Answer") and question.strip():
    with st.spinner("Looking for the answer..."):
        answer = get_answer(question)
        st.markdown("### 💬 Answer")
        st.write(answer)