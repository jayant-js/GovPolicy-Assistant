from data.loaders import load_pdfs
from splitters.recursive_splitter import split_documents
from vector_store.vector_db import create_vectorstore  
from langchain_groq import ChatGroq
from config.logger import get_logger
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain 
from config.config_loader import load_config
import os

config = load_config()
logger = get_logger(__name__)
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
You are a helpful and highly skilled financial analyst. Your tone should be professional, clear, and human. 
Your task is to answer the user's question by synthesizing the key information from the provided financial documents. 

**Structure your response like a professional briefing note:**

1.  **Summary First:** Begin with a concise paragraph that gives the main, bottom-line answer to the user's question.

2.  **Key Details:** Follow the summary with the most important supporting details.
    - Present these details as clear bullet points for readability.
    - Use **bolding** for emphasis on important names, figures, or dates.
    - **Consolidate information** if it's repeated in the documents. Do not state the same fact multiple times.

3.  **Grounding and Integrity:**
    - Every piece of information must come **exclusively** from the provided context.
    - To ensure accuracy, you **must add a source citation** after each fact or figure.
    - If you cannot find the answer in the context, simply state: "I do not have sufficient information to answer this."

### Context:
{context}

### User Query:
{input}

### Briefing Note:
""",
    input_variables=['context', 'input']
)

class BudgetRAGTrainingPipeline:
    def __init__(self, vectorstore_dir = config['vector_store']['persist_directory']):
        self.vectorstore_dir = vectorstore_dir
        self.docs = None

    def prepare_docs(self):
        logger.info('Loading PDFs...')
        self.docs = load_pdfs()
        logger.info(f'Loaded {len(self.docs)} documents')

        logger.info("Splitting documents into chunks...")
        self.docs = split_documents(self.docs)
        logger.info(f'Total chunks after splitting: {len(self.docs)}')

    def build_vectorstore(self):
        if self.docs is None:
            self.prepare_docs()
        logger.info("Creating FAISS vector store from documents...")
        retriever = create_vectorstore(self.docs)
        logger.info("Vector store creation complete.")
        return retriever

class BudgetRAGInferencePipeline:
    def __init__(self, llm_model='llama-3.3-70b-versatile', temperature=0.2, vectorstore_dir=config['vector_store']['persist_directory']):
        self.llm = ChatGroq(model=llm_model, temperature=temperature)
        self.vectorstore_dir = vectorstore_dir
        self.retriever = None
        self.qa_chain = None

    def load_vectorstore(self):
        from embeddings.create_embeddings import create_embedder
        from langchain_community.vectorstores import FAISS
        embedder = create_embedder()
        if os.path.exists(self.vectorstore_dir) and os.listdir(self.vectorstore_dir):
            logger.info(f"Loading existing FAISS vector store from {self.vectorstore_dir}")
            vector_store = FAISS.load_local(self.vectorstore_dir, embedder, allow_dangerous_deserialization=True)
            self.retriever = vector_store.as_retriever(
                search_type='mmr', search_kwargs={'k': 10, 'lambda_mult': 0.5, 'fetch_k': 20}
            )
        else:
            raise FileNotFoundError(f"No vector store found at {self.vectorstore_dir}. Please run training pipeline first.")
    
    def create_qa_chain(self):
        if not self.retriever:
            raise ValueError("Retriever not loaded. Call `load_vectorstore()` first.")
        logger.info("Creating QA chain for inference...")
        combine_docs_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt
        )
        self.qa_chain = create_retrieval_chain(
            retriever=self.retriever,
            combine_docs_chain=combine_docs_chain
        )
        logger.info("QA chain ready.")
    
    def query(self, question):
        if not self.qa_chain:
            raise ValueError("QA chain not created. Call `create_qa_chain()` first.")
        logger.info(f"Querying: {question}")
        result = self.qa_chain.invoke({'input': question})
        return result