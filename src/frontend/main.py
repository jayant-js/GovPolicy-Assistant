import streamlit as st
import requests
import os

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
            answer = data.get("answer", "Sorry, I couldn't find an answer.")
            sources = data.get("source_documents", [])
            return answer, sources
        else:
            return f"API Error {response.status_code}: {response.text}", []
    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}", []
    except Exception as e:
        return f"Unexpected error: {e}", []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]["answer"])
        if message["role"] == "assistant" and message["content"]["sources"]:
            st.markdown("---")
            for idx, doc in enumerate(message["content"]["sources"], 1):
                source_name = os.path.basename(doc.get('metadata', {}).get('source', 'Unknown'))
                with st.expander(f"Source {idx}: `{source_name}`"):
                    st.info(doc.get('page_content', 'No content available.'))

if prompt := st.chat_input("What is your question?"):
    user_message = {"role": "user", "content": {"answer": prompt, "sources": []}}
    st.session_state.messages.append(user_message)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents and generating an answer..."):
            answer, sources = get_answer(prompt)
            
            st.markdown(answer)
            
            if sources:
                st.markdown("---")
                for idx, doc in enumerate(sources, 1):
                    source_name = os.path.basename(doc.get('metadata', {}).get('source', 'Unknown'))
                    with st.expander(f"Source {idx}: `{source_name}`"):
                        st.info(doc.get('page_content', 'No content available.'))

            assistant_message = {"role": "assistant", "content": {"answer": answer, "sources": sources}}
            st.session_state.messages.append(assistant_message)