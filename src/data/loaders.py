from langchain_community.document_loaders import UnstructuredPDFLoader
from config.logger import get_logger

logger = get_logger(__name__)

pdfs = [
    "../data/Finance_Bill.pdf",
    "../data/Budget_Speech.pdf",
    "../data/explaining_finance_bill.pdf", 
    "../data/key_highlights.pdf"
]

def load_pdfs():
    all_docs = []
    for pdf_path in pdfs:
        logger.info(f"Loading PDF: {pdf_path}")
        loader = UnstructuredPDFLoader(pdf_path, strategy='auto', unstructured_kwargs={"languages": ["eng"]})
        docs = loader.load()
        all_docs.extend(docs)
    logger.info('Loaded all the pdfs')  
    return all_docs