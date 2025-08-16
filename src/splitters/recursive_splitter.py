from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.config_loader import load_config
from config.logger import get_logger
from data.loaders import load_pdfs

logger = get_logger(__name__)
config = load_config()

def get_text_splitter():
    chunk_size = config['splitters']['chunk_size']  
    chunk_overlap = config['splitters']['chunk_overlap']

    logger.info(f"Initializing text splitter with chunk size = {chunk_size}, and chunk overlap = {chunk_overlap}")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return splitter

def split_documents(docs):
    splitter = get_text_splitter()
    split_docs = splitter.split_documents(docs)
    logger.info(f"Total chunks after splitting: {len(split_docs)}")
    return split_docs