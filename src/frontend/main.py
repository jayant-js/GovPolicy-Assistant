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

show_sources = st.sidebar.checkbox("Show source documents", value=True)

question = st.text_input("Type your question here:")

def get_answer(question_text):
    try:
        payload = {"question": question_text}
        response = requests.post(api_url, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "Sorry, I couldn't find an answer.")
            sources = data.get("source_documents", [])
            return answer, sources
        else:
            return f"Error {response.status_code}: {response.text}", []
    except Exception as e:
        return f"An error occurred: {e}", []

if st.button("Get Answer") and question.strip():
    with st.spinner("Looking for the answer..."):
        answer, sources = get_answer(question)
        st.markdown("### 💬 Answer")
        st.write(answer)

        if show_sources and sources:
            st.markdown("#### 📄 Source Documents")
            for idx, doc in enumerate(sources, 1):
                source_name = doc.metadata.get('source', 'Unknown')
                st.markdown(f"**Document {idx}: {source_name}**")
                st.write(doc.page_content)