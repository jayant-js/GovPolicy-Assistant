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
prompt = PromptTemplate(
    template="""
    You are a financial assistant. Use the provided context to answer the query concisely.
    If there is sufficient context to answer the query, then only give the response, otherwise say: Insufficient Context.
    Context: \n
    {context}

    Query:
    {input}
"""
, input_variables=['context', 'input'])

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
            vector_store = FAISS.load_local(self.vectorstore_dir, embedder)
            self.retriever = vector_store.as_retriever(
                search_type='mmr', search_kwargs={'k': 5, 'lambda_mult': 0.25, 'fetch_k': 10}
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