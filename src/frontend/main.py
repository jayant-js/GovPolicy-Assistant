import streamlit as st
import requests

st.set_page_config(
    page_title="PolicyRAG - Budget 2025 Assistant",
    layout="centered",
)

st.title("PolicyRAG - Budget 2025 Assistant")
st.markdown(
    "Ask any question about the Union Budget 2025 and get clear, source-backed answers."
)

api_url = "https://policyrag.onrender.com/query"
question = st.text_input(
    "Type your question here:", 
    placeholder="e.g., What are the new policy schemes in Budget 2025?"
)

def get_answer(question_text):
    try:
        payload = {"question": question_text}
        response = requests.post(api_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "Sorry, I couldn't find an answer.")
            return answer
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return "Failed to get an answer from the backend.", []
            
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the API. Please ensure the backend is running. Error: {e}")
        return "An error occurred while trying to reach the backend service.", []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred.", []

if st.button("Get Answer", type="primary") and question.strip():
    with st.spinner("Analyzing documents and generating an answer..."):
        answer = get_answer(question)
        st.markdown("---")
        answer_container = st.container()
        with answer_container:
            st.markdown("### 💬 Answer")
            st.write(answer)