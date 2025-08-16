from langchain_community.vectorstores import FAISS
from embeddings.create_embeddings import create_embedder
from config.logger import get_logger
from config.config_loader import load_config
import os

logger = get_logger(__name__)
config = load_config()

def create_vectorstore(docs):
    embedder = create_embedder()
    persist_dir = config['vector_store']['persist_directory']
    if docs is None:
        raise ValueError('No documents provided to create a new vector store!') 
    vector_store = FAISS.from_documents(documents=docs, embedding=embedder)
    vector_store.save_local(persist_dir)
    logger.info(f"Created and saved FAISS vector store at {persist_dir}")   
    logger.info('Creating retriever from vector store.')
    retriever = vector_store.as_retriever(search_type='mmr', search_kwargs={'k':5, 'lambda_mult': 0.25, 'fetch_k':10})
    logger.info('retriever created.')
    return retriever